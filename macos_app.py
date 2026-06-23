"""
AR Model Uploader - macOS Native Application
PyQt6を使用したネイティブGUIアプリケーション
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QFileDialog,
    QProgressBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QMessageBox, QDropEvent, QDragEnterEvent, QComboBox
)
from PyQt6.QtCore import Qt, QUrl, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QDragEnterEvent, QDropEvent, QIcon, QDesktopServices
from PyQt6.QtWebEngineWidgets import QWebEngineView

from google_drive_handler import GoogleDriveHandler, get_mime_type
from model_viewer_generator import ARModelViewerGenerator, get_3d_file_info

# Constants
APP_NAME = "AR Model Uploader"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


class UploadWorker(QThread):
    """Background worker for file upload"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, file_path, file_name, title, description):
        super().__init__()
        self.file_path = file_path
        self.file_name = file_name
        self.title = title
        self.description = description
        self.drive_handler = None
    
    def run(self):
        """Upload file in background"""
        try:
            # Initialize Google Drive
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
            if not os.path.exists(credentials_path):
                self.error.emit("credentials.json が見つかりません")
                return
            
            self.drive_handler = GoogleDriveHandler(credentials_path=credentials_path)
            
            # Get file info
            file_info = get_3d_file_info(self.file_path)
            file_ext = file_info['extension'].lower()
            mime_type = get_mime_type(file_ext)
            
            self.progress.emit(10)
            
            # Upload to Google Drive
            drive_file = self.drive_handler.upload_file(
                file_path=self.file_path,
                file_name=self.file_name,
                mime_type=mime_type
            )
            
            self.progress.emit(50)
            
            # Make file public
            file_id = drive_file.get('id')
            self.drive_handler.make_public(file_id)
            
            self.progress.emit(75)
            
            # Generate viewer
            download_url = self.drive_handler.get_public_download_url(file_id)
            viewer_html = ARModelViewerGenerator.generate_embed_html(
                glb_url=download_url,
                usdz_url=download_url if file_ext == 'usdz' else None,
                title=self.title,
                allow_ar=True,
                auto_rotate=True,
                camera_controls=True
            )
            
            self.progress.emit(90)
            
            # Generate embed code
            viewer_url = f"file://{os.path.join(os.getcwd(), 'viewers', f'{file_id}.html')}"
            embed_code = ARModelViewerGenerator.generate_iframe_embed(
                viewer_url=viewer_url,
                title=self.title
            )
            
            self.progress.emit(100)
            
            # Return result
            result = {
                'success': True,
                'file_id': file_id,
                'title': self.title,
                'file_name': self.file_name,
                'file_size_mb': file_info['size_mb'],
                'public_url': drive_file.get('webViewLink'),
                'download_url': download_url,
                'viewer_html': viewer_html,
                'embed_code': embed_code,
                'uploaded_at': datetime.now().isoformat()
            }
            
            self.finished.emit(result)
        
        except Exception as e:
            self.error.emit(str(e))


class ARModelUploaderApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.uploaded_models = []
        self.selected_file = None
        self.upload_worker = None
        self.init_ui()
        self.load_models()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        # Header
        header_label = QLabel(f"🎨 {APP_NAME}")
        header_font = QFont()
        header_font.setPointSize(24)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(self.create_upload_tab(), "📤 アップロード")
        tabs.addTab(self.create_viewer_tab(), "🎮 ビューアー")
        tabs.addTab(self.create_models_tab(), "📚 モデル一覧")
        tabs.addTab(self.create_settings_tab(), "⚙️ 設定")
        
        layout.addWidget(tabs)
        central_widget.setLayout(layout)
        
        # Set application icon (optional)
        self.setStyleSheet(self.get_stylesheet())
    
    def create_upload_tab(self):
        """Create upload tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # File selection area
        self.file_label = QLabel("📁 ファイルを選択またはドラッグ&ドロップ")
        self.file_label.setStyleSheet("""
            border: 2px dashed #667eea;
            padding: 40px;
            text-align: center;
            border-radius: 8px;
            background-color: #f7fafc;
        """)
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.file_label)
        
        # File button
        file_button = QPushButton("ファイルを選択")
        file_button.clicked.connect(self.select_file)
        layout.addWidget(file_button)
        
        # Title input
        layout.addWidget(QLabel("モデルタイトル:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("例: 新製品のARモデル")
        layout.addWidget(self.title_input)
        
        # Description input
        layout.addWidget(QLabel("説明:"))
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("このモデルについて説明してください...")
        self.description_input.setMaximumHeight(100)
        layout.addWidget(self.description_input)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Upload button
        self.upload_button = QPushButton("🚀 アップロード")
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #48bb78;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #38a169;
            }
        """)
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)
        
        # Result area
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setVisible(False)
        layout.addWidget(self.result_text)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_viewer_tab(self):
        """Create viewer tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Viewer selection
        viewer_layout = QHBoxLayout()
        viewer_layout.addWidget(QLabel("モデルを選択:"))
        self.viewer_combo = QComboBox()
        self.viewer_combo.currentIndexChanged.connect(self.load_viewer)
        viewer_layout.addWidget(self.viewer_combo)
        layout.addLayout(viewer_layout)
        
        # Web engine view for AR
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        widget.setLayout(layout)
        return widget
    
    def create_models_tab(self):
        """Create models list tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Models table
        self.models_table = QTableWidget()
        self.models_table.setColumnCount(5)
        self.models_table.setHorizontalHeaderLabels([
            "タイトル", "ファイル名", "サイズ (MB)", "アップロード日", "操作"
        ])
        self.models_table.horizontalHeader().setStretchLastSection(False)
        layout.addWidget(self.models_table)
        
        # Refresh button
        refresh_button = QPushButton("🔄 更新")
        refresh_button.clicked.connect(self.load_models)
        layout.addWidget(refresh_button)
        
        widget.setLayout(layout)
        return widget
    
    def create_settings_tab(self):
        """Create settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Google credentials path
        layout.addWidget(QLabel("Google Credentials (JSON):"))
        creds_layout = QHBoxLayout()
        self.creds_path = QLineEdit()
        self.creds_path.setText(os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json'))
        creds_layout.addWidget(self.creds_path)
        
        creds_button = QPushButton("参照...")
        creds_button.clicked.connect(self.select_credentials)
        creds_layout.addWidget(creds_button)
        layout.addLayout(creds_layout)
        
        # Google Drive Folder ID
        layout.addWidget(QLabel("Google Drive Folder ID (オプション):"))
        self.folder_id = QLineEdit()
        self.folder_id.setText(os.getenv('GOOGLE_DRIVE_FOLDER_ID', 'root'))
        layout.addWidget(self.folder_id)
        
        # Save settings button
        save_button = QPushButton("💾 設定を保存")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        
        # Info
        info_label = QLabel(
            "📌 Google Cloud Console で認証情報を設定し、\n"
            "credentials.json をダウンロードしてください。"
        )
        info_label.setStyleSheet("color: #718096; padding: 20px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def select_file(self):
        """Select file to upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "3D モデルを選択",
            "",
            "3D Models (*.glb *.usdz *.gltf *.obj);;All Files (*)"
        )
        
        if file_path:
            self.selected_file = file_path
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            self.file_label.setText(f"✅ {file_name} ({file_size:.2f}MB)")
    
    def upload_file(self):
        """Upload file to Google Drive"""
        if not self.selected_file:
            QMessageBox.warning(self, "エラー", "ファイルを選択してください")
            return
        
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "エラー", "タイトルを入力してください")
            return
        
        # Disable upload button
        self.upload_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Start upload worker
        file_name = os.path.basename(self.selected_file)
        self.upload_worker = UploadWorker(
            self.selected_file,
            file_name,
            title,
            self.description_input.toPlainText()
        )
        self.upload_worker.progress.connect(self.update_progress)
        self.upload_worker.finished.connect(self.upload_finished)
        self.upload_worker.error.connect(self.upload_error)
        self.upload_worker.start()
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def upload_finished(self, result):
        """Handle successful upload"""
        self.upload_button.setEnabled(True)
        
        # Store model info
        self.uploaded_models.append(result)
        
        # Show result
        result_text = f"""
✅ アップロード成功！

タイトル: {result['title']}
ファイル: {result['file_name']}
サイズ: {result['file_size_mb']}MB
File ID: {result['file_id']}

Google Drive: {result['public_url']}

埋め込みコード:
{result['embed_code']}
        """
        
        self.result_text.setText(result_text)
        self.result_text.setVisible(True)
        
        # Update models list
        self.load_models()
        
        # Save viewer HTML
        viewers_dir = Path("viewers")
        viewers_dir.mkdir(exist_ok=True)
        viewer_path = viewers_dir / f"{result['file_id']}.html"
        with open(viewer_path, 'w', encoding='utf-8') as f:
            f.write(result['viewer_html'])
        
        QMessageBox.information(self, "成功", "ファイルがアップロードされました！")
    
    def upload_error(self, error_msg):
        """Handle upload error"""
        self.upload_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "エラー", f"アップロード失敗: {error_msg}")
    
    def load_models(self):
        """Load models list"""
        self.models_table.setRowCount(0)
        self.viewer_combo.clear()
        
        for i, model in enumerate(self.uploaded_models):
            self.models_table.insertRow(i)
            
            self.models_table.setItem(i, 0, QTableWidgetItem(model['title']))
            self.models_table.setItem(i, 1, QTableWidgetItem(model['file_name']))
            self.models_table.setItem(i, 2, QTableWidgetItem(str(model['file_size_mb'])))
            
            upload_date = datetime.fromisoformat(model['uploaded_at']).strftime('%Y-%m-%d %H:%M')
            self.models_table.setItem(i, 3, QTableWidgetItem(upload_date))
            
            # Action button
            view_button = QPushButton("👁️ 表示")
            view_button.clicked.connect(lambda checked, fid=model['file_id']: self.show_model(fid))
            self.models_table.setCellWidget(i, 4, view_button)
            
            # Add to viewer combo
            self.viewer_combo.addItem(model['title'], model['file_id'])
    
    def load_viewer(self):
        """Load viewer for selected model"""
        if self.viewer_combo.currentIndex() < 0:
            return
        
        file_id = self.viewer_combo.currentData()
        self.show_model(file_id)
    
    def show_model(self, file_id):
        """Show model in web viewer"""
        viewer_path = Path("viewers") / f"{file_id}.html"
        if viewer_path.exists():
            self.web_view.setUrl(QUrl.fromLocalFile(str(viewer_path.absolute())))
    
    def select_credentials(self):
        """Select Google credentials file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "credentials.json を選択",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            self.creds_path.setText(file_path)
    
    def save_settings(self):
        """Save application settings"""
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.creds_path.text()
        os.environ['GOOGLE_DRIVE_FOLDER_ID'] = self.folder_id.text()
        
        QMessageBox.information(self, "成功", "設定が保存されました")
    
    def get_stylesheet(self):
        """Get application stylesheet"""
        return """
        QMainWindow {
            background-color: #f7fafc;
        }
        QLabel {
            color: #2d3748;
        }
        QPushButton {
            background-color: #667eea;
            color: white;
            padding: 8px;
            border-radius: 5px;
            font-weight: bold;
            border: none;
        }
        QPushButton:hover {
            background-color: #5568d3;
        }
        QPushButton:pressed {
            background-color: #4c63b6;
        }
        QLineEdit, QTextEdit, QTableWidget {
            border: 1px solid #e2e8f0;
            border-radius: 5px;
            padding: 5px;
            background-color: white;
        }
        QLineEdit:focus, QTextEdit:focus {
            border: 2px solid #667eea;
        }
        QTabBar::tab {
            background-color: #e2e8f0;
            padding: 8px 20px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #667eea;
            color: white;
        }
        """


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    window = ARModelUploaderApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
