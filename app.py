"""
AR Model Uploader - Flask Application
Main application for uploading and sharing AR 3D models
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from google_drive_handler import GoogleDriveHandler, get_mime_type
from model_viewer_generator import ARModelViewerGenerator, get_3d_file_info

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app initialization
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 104857600))  # 100MB default

# Upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'glb', 'usdz', 'gltf', 'obj'}

# Global variables
drive_handler = None
model_registry = {}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def initialize_google_drive():
    """Initialize Google Drive handler"""
    global drive_handler
    try:
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
        if os.path.exists(credentials_path):
            drive_handler = GoogleDriveHandler(
                credentials_path=credentials_path,
                drive_folder_id=os.getenv('GOOGLE_DRIVE_FOLDER_ID')
            )
            logger.info("✓ Google Drive handler initialized")
            return True
        else:
            logger.warning("⚠ credentials.json not found")
            return False
    except Exception as e:
        logger.error(f"✗ Failed to initialize Google Drive: {e}")
        return False


@app.route('/')
def index():
    """Home page - upload interface"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'google_drive_ready': drive_handler is not None
    })


@app.route('/api/upload', methods=['POST'])
def upload_model():
    """
    Upload 3D model file
    
    Expected form data:
    - file: 3D model file (GLB, USDZ, etc.)
    - title: Model title (optional)
    - description: Model description (optional)
    """
    
    try:
        # Validate file
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Get metadata
        title = request.form.get('title', 'AR Model')
        description = request.form.get('description', '')
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        logger.info(f"✓ File saved: {file_path}")
        
        # Get file info
        file_info = get_3d_file_info(file_path)
        file_ext = file_info['extension'].lower()
        mime_type = get_mime_type(file_ext)
        
        # Upload to Google Drive if configured
        drive_file = None
        public_url = None
        embed_code = None
        download_url = None
        
        if drive_handler:
            try:
                # Upload file
                drive_file = drive_handler.upload_file(
                    file_path=file_path,
                    file_name=filename,
                    mime_type=mime_type
                )
                
                file_id = drive_file.get('id')
                logger.info(f"✓ Uploaded to Google Drive: {file_id}")
                
                # Make file public
                drive_handler.make_public(file_id)
                logger.info(f"✓ File made public: {file_id}")
                
                # Get public URLs
                public_url = drive_file.get('webViewLink')
                download_url = drive_handler.get_public_download_url(file_id)
                
                # Generate viewer HTML
                viewer_html = ARModelViewerGenerator.generate_embed_html(
                    glb_url=download_url,
                    usdz_url=download_url if file_ext == 'usdz' else None,
                    title=title,
                    allow_ar=True,
                    auto_rotate=True,
                    camera_controls=True
                )
                
                # Save viewer HTML temporarily
                viewer_filename = f"viewer_{timestamp[:-1]}.html"
                viewer_path = os.path.join(app.config['UPLOAD_FOLDER'], viewer_filename)
                with open(viewer_path, 'w', encoding='utf-8') as f:
                    f.write(viewer_html)
                
                # Generate embed code
                viewer_url = f"{request.host_url}api/viewer/{file_id}"
                embed_code = ARModelViewerGenerator.generate_iframe_embed(
                    viewer_url=viewer_url,
                    title=title,
                    width="100%",
                    height="600px"
                )
                
                # Register model
                model_registry[file_id] = {
                    'file_id': file_id,
                    'title': title,
                    'description': description,
                    'file_name': filename,
                    'file_ext': file_ext,
                    'file_info': file_info,
                    'drive_file': drive_file,
                    'viewer_html': viewer_html,
                    'uploaded_at': datetime.now().isoformat()
                }
                
                return jsonify({
                    'success': True,
                    'file_id': file_id,
                    'title': title,
                    'file_name': filename,
                    'file_size_mb': file_info['size_mb'],
                    'public_url': public_url,
                    'download_url': download_url,
                    'viewer_url': viewer_url,
                    'embed_code': embed_code,
                    'viewer_html': viewer_html,
                    'message': 'File uploaded and made public successfully'
                }), 200
            
            except Exception as e:
                logger.error(f"✗ Google Drive operation failed: {e}")
                return jsonify({
                    'error': f'Google Drive operation failed: {str(e)}',
                    'file_path': file_path
                }), 500
        
        else:
            # No Google Drive configured, return local file info
            logger.warning("⚠ Google Drive not configured, using local storage")
            
            return jsonify({
                'success': True,
                'message': 'File uploaded successfully (Google Drive not configured)',
                'file_name': filename,
                'file_path': file_path,
                'file_info': file_info,
                'warning': 'Configure Google Drive to enable public sharing'
            }), 200
    
    except Exception as e:
        logger.error(f"✗ Upload error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/viewer/<file_id>')
def viewer(file_id):
    """
    Serve AR viewer HTML for a specific model
    
    Args:
        file_id: Google Drive file ID
    """
    
    try:
        if file_id not in model_registry:
            return render_template('error.html', 
                                 error='Model not found',
                                 message='The requested model could not be found'), 404
        
        model_data = model_registry[file_id]
        viewer_html = model_data['viewer_html']
        
        return viewer_html, 200, {'Content-Type': 'text/html; charset=utf-8'}
    
    except Exception as e:
        logger.error(f"✗ Viewer error: {e}")
        return render_template('error.html',
                             error='Viewer error',
                             message=str(e)), 500


@app.route('/api/models', methods=['GET'])
def get_models():
    """Get list of uploaded models"""
    
    try:
        models = []
        for file_id, model_data in model_registry.items():
            models.append({
                'file_id': file_id,
                'title': model_data['title'],
                'description': model_data['description'],
                'file_name': model_data['file_name'],
                'file_size_mb': model_data['file_info']['size_mb'],
                'uploaded_at': model_data['uploaded_at'],
                'viewer_url': f"{request.host_url}api/viewer/{file_id}"
            })
        
        return jsonify({
            'success': True,
            'total': len(models),
            'models': models
        }), 200
    
    except Exception as e:
        logger.error(f"✗ Error fetching models: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/embed-instructions/<file_id>')
def embed_instructions(file_id):
    """Get embedding instructions for Google Sites"""
    
    try:
        if file_id not in model_registry:
            return jsonify({'error': 'Model not found'}), 404
        
        viewer_url = f"{request.host_url}api/viewer/{file_id}"
        instructions = ARModelViewerGenerator.generate_google_sites_embed_instructions(viewer_url)
        
        return jsonify({
            'success': True,
            'instructions': instructions,
            'embed_code': ARModelViewerGenerator.generate_iframe_embed(viewer_url),
            'viewer_url': viewer_url
        }), 200
    
    except Exception as e:
        logger.error(f"✗ Error generating instructions: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/delete/<file_id>', methods=['DELETE'])
def delete_model(file_id):
    """Delete model from Google Drive and registry"""
    
    try:
        if file_id not in model_registry:
            return jsonify({'error': 'Model not found'}), 404
        
        if drive_handler:
            drive_handler.delete_file(file_id)
        
        del model_registry[file_id]
        
        return jsonify({
            'success': True,
            'message': 'Model deleted successfully'
        }), 200
    
    except Exception as e:
        logger.error(f"✗ Error deleting model: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'error': 'File too large',
        'message': f'Maximum file size is {app.config["MAX_CONTENT_LENGTH"] / (1024*1024):.0f}MB'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 error"""
    return jsonify({'error': 'Not found', 'message': str(error)}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 error"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("AR Model Uploader Starting...")
    logger.info("=" * 50)
    
    # Initialize Google Drive
    initialize_google_drive()
    
    # Get configuration
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"📱 Server running at http://{host}:{port}")
    logger.info(f"🔧 Debug mode: {debug}")
    logger.info(f"📁 Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    
    # Start server
    app.run(host=host, port=port, debug=debug)
