# 🎨 AR Model Uploader - macOS版

Google WorkspaceのWebサイトにAR 3Dモデル（USDZ/GLB）をアップロード・公開するmacOS ネイティブアプリケーション

## 🌟 特徴

- ✅ **macOS ネイティブGUI** - PyQt6を使用した美しいインターフェース
- ✅ **ドラッグ&ドロップ対応** - ファイルをドラッグするだけでアップロード
- ✅ **Google Drive統合** - 自動的にGoogle Driveにアップロード＆公開
- ✅ **AR体験プレビュー** - アプリ内でAR体験を確認
- ✅ **複数フォーマット対応** - GLB、USDZ、GLTF、OBJ
- ✅ **ワンクリック埋め込み** - Google Sitesへ簡単に埋め込み
- ✅ **iOS/Android両対応** - iOSはAR Quick Look、AndroidはWebAR

## 📋 システム要件

- **macOS 10.15+** (Catalina以上)
- **Python 3.8+**
- **Google Workspace アカウント**
- **Google Cloud Platform アカウント**

## 🚀 インストール手順

### 1. リポジトリをクローン

```bash
git clone https://github.com/wintermute-HC/ar-model-uploader.git
cd ar-model-uploader
```

### 2. セットアップスクリプトを実行

```bash
chmod +x setup_macos.sh
./setup_macos.sh
```

このスクリプトが以下を実施します：
- Python 3 のインストール確認
- Python仮想環境の作成
- 依存パッケージのインストール
- 必要なディレクトリの作成
- 環境変数ファイルの初期化

### 3. Google Cloud認証情報を設定

#### ステップA: Google Cloud Consoleでプロジェクト作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. **プロジェクトを作成** をクリック
3. プロジェクト名を入力（例: `ar-model-uploader`）
4. **作成** をクリック

#### ステップB: Google Drive APIを有効化

1. 左サイドバーの **API とサービス** → **ライブラリ** をクリック
2. 検索ボックスで「Google Drive API」を検索
3. 検索結果から **Google Drive API** をクリック
4. **有効にする** をクリック

#### ステップC: サービスアカウント キーを作成

1. 左サイドバーの **API とサービス** → **認証情報** をクリック
2. **認証情報を作成** → **サービスアカウント** をクリック
3. サービスアカウント詳細を入力：
   - サービスアカウント名: `ar-model-uploader`
   - サービスアカウントID: 自動生成
4. **作成して続行** をクリック
5. ロール選択ページで **Editor** ロールを選択（簡易設定）
6. **続行** → **完了** をクリック

#### ステップD: キーをJSON形式でダウンロード

1. 作成したサービスアカウントをクリック
2. **キー** タブをクリック
3. **キーを追加** → **新しいキーを作成** をクリック
4. **JSON** を選択
5. **作成** をクリック
6. JSONファイルが自動ダウンロードされます

#### ステップE: credentials.jsonをプロジェクトに配置

```bash
# ダウンロードしたファイルをプロジェクトディレクトリにコピー
cp ~/Downloads/[downloaded-file].json ./credentials.json
```

### 4. 環境変数を設定

```bash
nano .env
```

以下の内容を編集：

```env
# Google Cloud Setup
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
GOOGLE_DRIVE_FOLDER_ID=root  # または特定のフォルダID

# Flask Setup
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# File Upload Settings
MAX_FILE_SIZE=104857600  # 100MB in bytes
ALLOWED_EXTENSIONS=glb,usdz

# Server Settings
HOST=0.0.0.0
PORT=5000
```

**Ctrl+X** → **Y** → **Enter** で保存

## 🎮 アプリケーション起動

### 方法1: スクリプトで起動（推奨）

```bash
./run.sh
```

### 方法2: 直接実行

```bash
source venv/bin/activate
python3 macos_app.py
```

アプリケーションが起動し、以下のウィンドウが表示されます：

```
┌─────────────────────────────────────┐
│  🎨 AR Model Uploader v1.0.0        │
├─────────────────────────────────────┤
│ [📤 アップロード] [🎮 ビューアー]   │
│ [📚 モデル一覧]  [⚙️ 設定]         │
└─────────────────────────────────────┘
```

## 📖 使用方法

### 1️⃣ アップロードタブ

1. **ファイルを選択** ボタンをクリックまたはドラッグ&ドロップ
2. USDZ または GLB ファイルを選択
3. **モデルタイトル** を入力
4. （オプション）**説明** を入力
5. **🚀 アップロード** をクリック

**対応フォーマット：**
- ✅ GLB (.glb) - Android・PC対応
- ✅ USDZ (.usdz) - iOS AR Quick Look対応
- ✅ GLTF (.gltf) - JSON形式のglTF
- ✅ OBJ (.obj) - ウェーブフロント形式

**最大ファイルサイズ：** 100MB

### 2️⃣ ビューアータブ

1. **モデルを選択** ドロップダウンからモデルを選択
2. 3Dビューアーでモデルが表示されます
3. マウスでドラッグして回転
4. スクロールで拡大/縮小
5. **📱 AR で見る** ボタンで実デバイスでAR表示

### 3️⃣ モデル一覧タブ

- アップロード済みの全モデルが表示
- **👁️ 表示** ボタンでビューアーを開く
- モデルの詳細情報を確認可能

### 4️⃣ 設定タブ

- Google Credentials パスを設定
- Google Drive Folder ID を設定
- **💾 設定を保存** で変更を反映

## 🌐 Google Sitesへの埋め込み

### ステップ1: 埋め込みコードをコピー

1. アップロード成功後、埋め込みコードが表示されます
2. **コピー** ボタンをクリック

### ステップ2: Google Sitesに埋め込み

1. [Google Sites](https://sites.google.com/) にアクセス
2. Webサイトを開く
3. 編集モードに切り替え
4. **挿入** → **埋め込み** → **URLから埋め込む** をクリック
5. コピーしたURLを貼り付け
6. **次へ** → **挿入** をクリック

### ステップ3: 公開

1. **公開** ボタンをクリック
2. 共有リンクをコピー
3. リンクを配布

## 📱 デバイス別AR体験

### iOS (iPhone/iPad)

1. **Safari** でWebサイトを開く
2. AR対応モデルで **📱 AR で見る** をタップ
3. **AR Quick Look** が起動
4. 周囲をスキャンしてAR表示

**必要条件：** iOS 12.0+、LiDAR搭載デバイス推奨

### Android

1. **Chrome** または **Samsung Internet** で開く
2. **📱 AR で見る** をタップ
3. カメラ権限を許可
4. AR表示が開始

**必要条件：** Android 7.0+、ARCore対応デバイス

## 🔧 トラブルシューティング

### ❌ `credentials.json not found`

**解決策：**
```bash
# Google Cloud Consoleから credentials.json をダウンロード
cp ~/Downloads/[downloaded-file].json ./credentials.json
```

### ❌ `Permission denied` エラー

**解決策：**
```bash
# 権限を付与
chmod +x setup_macos.sh run.sh
```

### ❌ `Port 5000 is already in use`

**解決策：** .env で PORT を変更
```env
PORT=5001
```

### ❌ Python モジュールが見つからない

**解決策：**
```bash
# 仮想環境を有効化
source venv/bin/activate

# 依存パッケージを再インストール
pip install -r requirements.txt
```

### ❌ PyQt6 が起動しない

**解決策：**
```bash
# PyQt6 とWebEngine を再インストール
pip install --upgrade PyQt6 PyQt6-WebEngine
```

## 📊 プロジェクト構成

```
ar-model-uploader/
├── macos_app.py                    # macOS ネイティブアプリケーション
├── app.py                          # Flask Webサーバー
├── google_drive_handler.py         # Google Drive API
├── model_viewer_generator.py       # AR HTML生成
├── requirements.txt                # Python依存パッケージ
├── .env.example                    # 環境変数テンプレート
├── setup_macos.sh                  # macOSセットアップスクリプト
├── run.sh                          # 起動スクリプト
├── templates/
│   ├── index.html                  # Webインターフェース
│   ├── viewer.html                 # AR ビューアー
│   └── success.html                # 成功画面
├── static/
│   ├── css/style.css               # スタイルシート
│   └── js/script.js                # フロントエンド JS
├── uploads/                        # アップロード一時保存
├── viewers/                        # AR ビューアーHTML
└── README.md                       # このファイル
```

## 🎓 対応ファイル形式詳細

### GLB (glTF Binary)
- **対応デバイス：** Android、Windows、macOS、Linux
- **ファイルサイズ：** 比較的小さい（圧縮形式）
- **特徴：** バイナリ形式で高速ロード
- **用途：** WebAR全般

### USDZ (Universal Scene Description Zipped)
- **対応デバイス：** iOS（AR Quick Look）
- **ファイルサイズ：** 中程度
- **特徴：** Pixarが開発した形式
- **用途：** iPhone/iPad AR体験

### GLTF (glTF JSON)
- **対応デバイス：** Web標準対応全般
- **ファイルサイズ：** JSONベース（やや大きい）
- **特徴：** テキスト形式で編集可能
- **用途：** デバッグ、カスタマイズ

### OBJ (Wavefront)
- **対応デバイス：** Web対応ブラウザ
- **ファイルサイズ：** 大きい（テキスト形式）
- **特徴：** 古い形式だが広範に対応
- **用途：** 互換性重視

## 🔒 セキュリティ注意事項

1. **credentials.json は絶対に公開しない**
   - Git リポジトリにコミットしない
   - `.gitignore` に追加

2. **Google Drive Folder ID を限定する**
   - 特定のフォルダに限定して公開

3. **ファイルサイズ制限を設定**
   - デフォルト: 100MB

4. **アップロード権限を制限**
   - 本番環境では認証機構を追加

## 📚 参考リンク

- [Google Model Viewer](https://modelviewer.dev/)
- [Google Drive API ドキュメント](https://developers.google.com/drive/api)
- [USDZ 形式 - Apple](https://developer.apple.com/usdz/)
- [glTF 形式 - Khronos](https://www.khronos.org/gltf/)
- [PyQt6 ドキュメント](https://www.riverbankcomputing.com/static/Docs/PyQt6/)

## 🤝 コントリビューション

改善提案やバグ報告は、[Issues](https://github.com/wintermute-HC/ar-model-uploader/issues) でお願いします。

## 📄 ライセンス

MIT License

## 👨‍💻 作成者

wintermute-HC

## 📞 サポート

問題が発生した場合：

1. [Issues](https://github.com/wintermute-HC/ar-model-uploader/issues) で検索
2. 解決しない場合は新規 Issue を作成
3. 詳細なエラーログを添付

---

**バージョン:** 1.0.0  
**最終更新:** 2026年6月23日  
**開発環境：** Python 3.8+, PyQt6, Flask, Google Drive API
