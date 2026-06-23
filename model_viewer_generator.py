"""
AR Model Viewer HTML Generator
Generates HTML pages for AR 3D model viewing
"""

import os
from datetime import datetime


class ARModelViewerGenerator:
    """Generate AR-enabled HTML viewers for 3D models"""
    
    MODEL_VIEWER_CDN = "https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"
    
    def __init__(self):
        """Initialize the generator"""
        self.generated_viewers = {}
    
    @staticmethod
    def generate_embed_html(glb_url, usdz_url=None, title="AR Model", 
                           allow_ar=True, auto_rotate=True, camera_controls=True):
        """
        Generate embed-ready HTML for AR viewer
        
        Args:
            glb_url: URL to GLB model file
            usdz_url: URL to USDZ model file (for iOS)
            title: Model title
            allow_ar: Enable AR viewing
            auto_rotate: Enable auto-rotation
            camera_controls: Enable camera controls
        
        Returns:
            str: HTML code ready to embed
        """
        
        usdz_attr = f'ios-src="{usdz_url}"' if usdz_url else ''
        ar_attr = 'ar' if allow_ar else ''
        auto_rotate_attr = 'auto-rotate' if auto_rotate else ''
        camera_controls_attr = 'camera-controls' if camera_controls else ''
        
        html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script type="module" src="{ARModelViewerGenerator.MODEL_VIEWER_CDN}"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        
        .container {{
            width: 100%;
            max-width: 900px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 8px;
        }}
        
        .header p {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .viewer-wrapper {{
            position: relative;
            width: 100%;
            padding-bottom: 100%;
            height: 0;
            background: #f5f5f5;
        }}
        
        model-viewer {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(180deg, #e0e0e0 0%, #f5f5f5 100%);
        }}
        
        .controls {{
            padding: 20px 30px;
            background: #fafafa;
            border-top: 1px solid #e0e0e0;
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }}
        
        .controls button {{
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            background: #667eea;
            color: white;
            font-size: 14px;
            cursor: pointer;
            transition: background 0.3s;
        }}
        
        .controls button:hover {{
            background: #764ba2;
        }}
        
        .info {{
            padding: 20px 30px;
            background: white;
            border-top: 1px solid #e0e0e0;
            font-size: 13px;
            color: #666;
        }}
        
        .info p {{
            margin: 8px 0;
        }}
        
        .badge {{
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-right: 8px;
        }}
        
        @media (max-width: 768px) {{
            .header {{
                padding: 20px;
            }}
            
            .header h1 {{
                font-size: 22px;
            }}
            
            .controls {{
                padding: 15px 20px;
            }}
            
            .controls button {{
                padding: 8px 16px;
                font-size: 13px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 AR 3D モデルビューアー</h1>
            <p>拡張現実で3Dモデルを体験</p>
        </div>
        
        <div class="viewer-wrapper">
            <model-viewer 
                src="{glb_url}"
                {usdz_attr}
                {ar_attr}
                {auto_rotate_attr}
                {camera_controls_attr}
                shadow-intensity="1"
                exposure="1"
                enable-lighting>
            </model-viewer>
        </div>
        
        <div class="controls">
            <button onclick="document.querySelector('model-viewer').resetCamera()">
                🔄 カメラをリセット
            </button>
            {('<button onclick="launchAR()">📱 AR で見る</button>' if allow_ar else '')}
            <button onclick="downloadModel()">
                ⬇️ ダウンロード
            </button>
        </div>
        
        <div class="info">
            <p>
                <span class="badge">GLB対応</span>
                <span class="badge">Android</span>
                {('<span class="badge">USDZ対応</span>' if usdz_url else '')}
                {('<span class="badge">iOS AR</span>' if usdz_url else '')}
            </p>
            <p>💡 ヒント: マウスでドラッグして回転 | スクロールで拡大/縮小 | タッチで操作</p>
            <p>⏰ 作成日: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
        </div>
    </div>
    
    <script>
        function launchAR() {{
            const modelViewer = document.querySelector('model-viewer');
            modelViewer.activateAR();
        }}
        
        function downloadModel() {{
            const modelViewer = document.querySelector('model-viewer');
            const src = modelViewer.src;
            if (src) {{
                const a = document.createElement('a');
                a.href = src;
                a.download = 'model.glb';
                a.click();
            }}
        }}
        
        // Error handling
        document.querySelector('model-viewer').addEventListener('error', (e) => {{
            console.error('Model Viewer Error:', e);
        }});
    </script>
</body>
</html>'''
        
        return html
    
    @staticmethod
    def generate_iframe_embed(viewer_url, title="AR Model", width="100%", height="600px"):
        """
        Generate iframe embed code for Google Sites
        
        Args:
            viewer_url: URL to the AR viewer page
            title: Model title
            width: iframe width
            height: iframe height
        
        Returns:
            str: iframe HTML code
        """
        
        iframe = f'<iframe src="{viewer_url}" title="{title}" width="{width}" height="{height}" style="border: none; border-radius: 8px;" allow="camera; display-capture; xr-spatial-tracking"></iframe>'
        
        return iframe
    
    @staticmethod
    def generate_google_sites_embed_instructions(viewer_url):
        """
        Generate instructions for embedding in Google Sites
        
        Args:
            viewer_url: URL to the AR viewer page
        
        Returns:
            str: Markdown formatted instructions
        """
        
        instructions = f"""# Google Sites へのAR モデル埋め込み方法

## 埋め込みコード
```html
{ARModelViewerGenerator.generate_iframe_embed(viewer_url)}
```

## 手順

1. **Google Sitesにアクセス** → 編集モードを開く
2. **「挿入」** メニューをクリック
3. **「埋め込み」** → **「URLから埋め込む」** を選択
4. 以下のURLを貼り付け:
   ```
   {viewer_url}
   ```

## または

1. **「挿入」** メニューをクリック
2. **「埋め込み」** → **「コードを埋め込む」** を選択
3. 上記の埋め込みコードを貼り付け
4. **「次へ」** → **「挿入」**

---

## 動作確認

- ✅ **PC (Windows/Mac)**: Chrome, Firefox, Safari
- ✅ **Android**: Chrome, Samsung Internet
- ✅ **iOS**: Safari (AR Quick Look)

## トラブルシューティング

- **AR が動作しない**: 
  - iOSの場合、Safari で USDZ ファイルが必要です
  - Androidの場合、WebARに対応したブラウザが必要です

- **モデルが読み込まない**:
  - ファイルサイズを確認 (100MB以下)
  - ネットワーク接続を確認
  - ブラウザキャッシュをクリア

---

**生成時刻**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return instructions
    
    @staticmethod
    def generate_mobile_link(glb_url, usdz_url=None, title="AR Model"):
        """
        Generate simple mobile-friendly link
        
        Args:
            glb_url: URL to GLB file
            usdz_url: URL to USDZ file
            title: Model title
        
        Returns:
            dict: Links for different platforms
        """
        
        links = {
            'glb_url': glb_url,
            'usdz_url': usdz_url,
            'ar_quick_look_ios': usdz_url if usdz_url else None,
            'viewer_html_generated': True,
            'title': title,
            'timestamp': datetime.now().isoformat()
        }
        
        return links


# Utility functions
def get_3d_file_info(file_path):
    """
    Extract information about 3D model file
    
    Args:
        file_path: Path to 3D model file
    
    Returns:
        dict: File information
    """
    
    if not os.path.exists(file_path):
        return None
    
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_name)[1].lower().strip('.')
    
    return {
        'name': file_name,
        'extension': file_ext,
        'size_bytes': file_size,
        'size_mb': round(file_size / (1024 * 1024), 2),
        'created_time': datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(),
        'modified_time': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
    }
