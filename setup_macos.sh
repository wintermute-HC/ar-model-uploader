#!/bin/bash

# AR Model Uploader - macOS Setup Script
# このスクリプトは、macOS上でAR Model Uploaderアプリケーションをセットアップします

set -e  # Exit on error

echo "=========================================="
echo "🎨 AR Model Uploader - macOS Setup"
echo "=========================================="
echo ""

# Check Python version
echo "🔍 Python バージョン確認中..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 がインストールされていません。"
    echo "   以下のコマンドで Homebrew をインストール後、Python3 をインストールしてください："
    echo "   brew install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "🔨 仮想環境を作成中..."
if [ -d "venv" ]; then
    echo "   仮想環境は既に存在します"
else
    python3 -m venv venv
    echo "✅ 仮想環境を作成しました"
fi
echo ""

# Activate virtual environment
echo "🚀 仮想環境を有効化中..."
source venv/bin/activate
echo "✅ 仮想環境を有効化しました"
echo ""

# Upgrade pip
echo "📦 pip をアップグレード中..."
pip install --upgrade pip
echo "✅ pip をアップグレードしました"
echo ""

# Install dependencies
echo "📚 依存パッケージをインストール中..."
pip install -r requirements.txt
echo "✅ 依存パッケージをインストールしました"
echo ""

# Create directories
echo "📁 必要なディレクトリを作成中..."
mkdir -p templates
mkdir -p static/css
mkdir -p static/js
mkdir -p uploads
mkdir -p viewers
echo "✅ ディレクトリを作成しました"
echo ""

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo "⚙️  環境変数ファイルを作成中..."
    cp .env.example .env
    echo "✅ .env ファイルを作成しました"
    echo "   📝 以下のコマンドで .env ファイルを編集してください："
    echo "   nano .env"
else
    echo "✅ .env ファイルは既に存在します"
fi
echo ""

# Create launch script
echo "📝 起動スクリプトを作成中..."
cat > run.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python3 macos_app.py
EOF
chmod +x run.sh
echo "✅ 起動スクリプトを作成しました"
echo ""

# Check Google credentials
echo "🔐 Google 認証情報を確認中..."
if [ -f "credentials.json" ]; then
    echo "✅ credentials.json が見つかりました"
else
    echo "⚠️  credentials.json が見つかりません"
    echo "   以下の手順で取得してください："
    echo "   1. https://console.cloud.google.com/ にアクセス"
    echo "   2. 新しいプロジェクトを作成"
    echo "   3. Google Drive API を有効化"
    echo "   4. サービスアカウント キーを作成（JSON形式）"
    echo "   5. ダウンロードしたファイルをプロジェクトディレクトリに配置"
fi
echo ""

echo "=========================================="
echo "✅ セットアップが完了しました！"
echo "=========================================="
echo ""
echo "📝 次のステップ："
echo "1. credentials.json を設定する（上記参照）"
echo "2. 以下のコマンドでアプリケーションを起動："
echo "   ./run.sh"
echo ""
echo "📚 詳細は README.md を参照してください"
echo ""
