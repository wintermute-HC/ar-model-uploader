"""
Google Drive API Handler
Manages file uploads and sharing permissions
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.auth.exceptions import DefaultCredentialsError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging

logger = logging.getLogger(__name__)

# Scopes for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDriveHandler:
    """Handle Google Drive API operations"""
    
    def __init__(self, credentials_path='credentials.json', drive_folder_id=None):
        """
        Initialize Google Drive Handler
        
        Args:
            credentials_path: Path to service account JSON file
            drive_folder_id: Parent folder ID in Google Drive
        """
        self.credentials_path = credentials_path
        self.drive_folder_id = drive_folder_id or os.getenv('GOOGLE_DRIVE_FOLDER_ID', 'root')
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API"""
        try:
            if not os.path.exists(self.credentials_path):
                raise FileNotFoundError(f"Credentials file not found: {self.credentials_path}")
            
            credentials = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=SCOPES
            )
            self.service = build('drive', 'v3', credentials=credentials)
            logger.info("✓ Google Drive API authenticated successfully")
        except FileNotFoundError as e:
            logger.error(f"✗ Authentication failed: {e}")
            raise
        except Exception as e:
            logger.error(f"✗ Authentication error: {e}")
            raise
    
    def upload_file(self, file_path, file_name=None, mime_type='model/gltf-binary'):
        """
        Upload file to Google Drive
        
        Args:
            file_path: Local file path
            file_name: Name for the file in Google Drive
            mime_type: MIME type (model/gltf-binary for GLB, model/vnd.usdz+zip for USDZ)
        
        Returns:
            dict: File ID and metadata
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if file_name is None:
                file_name = os.path.basename(file_path)
            
            file_metadata = {
                'name': file_name,
                'parents': [self.drive_folder_id]
            }
            
            media = MediaFileUpload(
                file_path,
                mimetype=mime_type,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink, webContentLink'
            ).execute()
            
            logger.info(f"✓ File uploaded successfully: {file.get('name')} (ID: {file.get('id')})")
            return file
        
        except Exception as e:
            logger.error(f"✗ Upload failed: {e}")
            raise
    
    def make_public(self, file_id):
        """
        Make file publicly accessible
        
        Args:
            file_id: Google Drive file ID
        
        Returns:
            dict: Permission metadata
        """
        try:
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            
            result = self.service.permissions().create(
                fileId=file_id,
                body=permission
            ).execute()
            
            logger.info(f"✓ File made public: {file_id}")
            return result
        
        except Exception as e:
            logger.error(f"✗ Failed to make file public: {e}")
            raise
    
    def get_file_info(self, file_id):
        """
        Get file information from Google Drive
        
        Args:
            file_id: Google Drive file ID
        
        Returns:
            dict: File metadata
        """
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields='id, name, webViewLink, webContentLink, mimeType, createdTime'
            ).execute()
            
            return file
        
        except Exception as e:
            logger.error(f"✗ Failed to get file info: {e}")
            raise
    
    def get_public_download_url(self, file_id):
        """
        Generate public download URL for the file
        
        Args:
            file_id: Google Drive file ID
        
        Returns:
            str: Direct download URL
        """
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    
    def delete_file(self, file_id):
        """
        Delete file from Google Drive
        
        Args:
            file_id: Google Drive file ID
        """
        try:
            self.service.files().delete(fileId=file_id).execute()
            logger.info(f"✓ File deleted: {file_id}")
        
        except Exception as e:
            logger.error(f"✗ Failed to delete file: {e}")
            raise


def get_mime_type(file_extension):
    """
    Get MIME type for 3D model file
    
    Args:
        file_extension: File extension (e.g., 'glb', 'usdz')
    
    Returns:
        str: MIME type
    """
    mime_types = {
        'glb': 'model/gltf-binary',
        'gltf': 'model/gltf+json',
        'usdz': 'model/vnd.usdz+zip',
        'obj': 'text/plain',
        'fbx': 'application/octet-stream'
    }
    
    return mime_types.get(file_extension.lower(), 'application/octet-stream')
