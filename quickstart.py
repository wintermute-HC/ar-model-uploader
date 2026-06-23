#!/usr/bin/env python3
"""
AR Model Uploader - Quick Start Script
macOS で簡単にセットアップ＆起動
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Print header text"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*50}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*50}{Colors.ENDC}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.OKBLUE}ℹ️  {text}{Colors.ENDC}")

def check_python():
    """Check Python version"""
    print_info("Python バージョン確認中...")
    
    try:
        result = subprocess.run(['python3', '--version'], 
                              capture_output=True, text=True)
        version = result.stdout.strip()
        print_success(f"{version}")
        return True
    except FileNotFoundError:
        print_error("Python3 がインストールされていません")
        print_warning("以下のコマンドで Homebrew を使用してインストールしてください:")
        print("   brew install python3")
        return False

def check_homebrew():
    """Check if Homebrew is installed"""
    print_info("Homebrew 確認中...")
    
    try:
        subprocess.run(['brew', '--version'], 
                      capture_output=True, check=True)
        print_success("Homebrew がインストールされています")
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print_warning("Homebrew がインストールされていません")
        print_info("以下のコマンドでインストールしてください:")
        print('   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
        return False

def create_venv():
    """Create virtual environment"""
    print_info("仮想環境を作成中...")
    
    if Path("venv").exists():
        print_success("仮想環境は既に存在します")
        return True
    
    try:
        subprocess.run(['python3', '-m', 'venv', 'venv'], 
                      check=True, capture_output=True)
        print_success("仮想環境を作成しました")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"仮想環境作成に失敗: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print_info("依存パッケージをインストール中...")
    print_warning("初回は数分かかります...")
    
    venv_pip = "venv/bin/pip"
    
    try:
        # Upgrade pip
        subprocess.run([venv_pip, 'install', '--upgrade', 'pip'],
                      check=True, capture_output=True)
        
        # Install requirements
        subprocess.run([venv_pip, 'install', '-r', 'requirements.txt'],
                      check=True, capture_output=False)
        
        print_success("依存パッケージをインストールしました")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"パッケージインストールに失敗: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print_info("ディレクトリを作成中...")
    
    directories = [
        'templates',
        'static/css',
        'static/js',
        'uploads',
        'viewers'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print_success("ディレクトリを作成しました")
    return True

def setup_env_file():
    """Setup .env file"""
    print_info("環境変数ファイルを設定中...")
    
    if Path(".env").exists():
        print_success(".env ファイルは既に存在します")
        return True
    
    if not Path(".env.example").exists():
        print_error(".env.example が見つかりません")
        return False
    
    try:
        with open(".env.example", "r") as src:
            content = src.read()
        with open(".env", "w") as dst:
            dst.write(content)
        
        print_success(".env ファイルを作成しました")
        print_warning("以下のコマンドで .env ファイルを編集してください:")
        print("   nano .env")
        return True
    except Exception as e:
        print_error(f"ファイル作成に失敗: {e}")
        return False

def check_credentials():
    """Check Google credentials"""
    print_info("Google 認証情報を確認中...")
    
    if Path("credentials.json").exists():
        print_success("credentials.json が見つかりました")
        return True
    
    print_warning("credentials.json が見つかりません")
    print_info("以下の手順で設定してください:")
    print()
    print("1️⃣  Google Cloud Console にアクセス")
    print("   https://console.cloud.google.com/")
    print()
    print("2️⃣  プロジェクトを作成")
    print("   - 'プロジェクトを作成' をクリック")
    print("   - プロジェクト名: ar-model-uploader")
    print()
    print("3️⃣  Google Drive API を有効化")
    print("   - API ライブラリを開く")
    print("   - 'Google Drive API' を検索")
    print("   - '有効にする' をクリック")
    print()
    print("4️⃣  サービスアカウントキーを作成")
    print("   - API とサービス > 認証情報")
    print("   - '認証情報を作成' > 'サービスアカウント'")
    print("   - サービスアカウント名: ar-model-uploader")
    print("   - ロール: Editor")
    print()
    print("5️⃣  JSONキーをダウンロード")
    print("   - サービスアカウントをクリック")
    print("   - 'キー' タブ")
    print("   - '新しいキーを作成' > JSON")
    print()
    print("6️⃣  credentials.json として保存")
    print("   - ダウンロードしたファイルをプロジェクトディレクトリにコピー")
    print()
    
    return False

def create_run_script():
    """Create run script"""
    print_info("起動スクリプトを作成中...")
    
    if Path("run.sh").exists():
        print_success("run.sh は既に存在します")
        return True
    
    try:
        with open("run.sh", "w") as f:
            f.write("""#!/bin/bash
source venv/bin/activate
python3 macos_app.py
""")
        
        os.chmod("run.sh", 0o755)
        print_success("起動スクリプトを作成しました")
        return True
    except Exception as e:
        print_error(f"スクリプト作成に失敗: {e}")
        return False

def create_alias():
    """Create shell alias for easy running"""
    print_info("シェルエイリアスを作成中...")
    
    shell_rc = Path.home() / ".zshrc"  # macOS default
    if not shell_rc.exists():
        shell_rc = Path.home() / ".bash_profile"
    
    if not shell_rc.exists():
        print_warning("シェル設定ファイルが見つかりません")
        return False
    
    try:
        with open(shell_rc, "r") as f:
            content = f.read()
        
        # Check if alias already exists
        if "alias ar-uploader" in content:
            print_success("エイリアスは既に設定されています")
            return True
        
        # Add alias
        project_path = os.getcwd()
        alias_line = f'\nalias ar-uploader="cd {project_path} && ./run.sh"\n'
        
        with open(shell_rc, "a") as f:
            f.write(alias_line)
        
        print_success("エイリアスを作成しました")
        print_info("ターミナルを再起動後、以下のコマンドで起動できます:")
        print("   ar-uploader")
        return True
    except Exception as e:
        print_warning(f"エイリアス作成に失敗: {e}")
        return False

def show_next_steps():
    """Show next steps"""
    print_header("🎉 セットアップが完了しました！")
    
    print_success("準備完了")
    print()
    print("📝 次のステップ:")
    print()
    print("1️⃣  credentials.json を設定")
    print("   Google Cloud Console で credentials.json をダウンロード")
    print("   プロジェクトディレクトリに配置してください")
    print()
    print("2️⃣  環境変数を設定（必要に応じて）")
    print("   nano .env")
    print()
    print("3️⃣  アプリケーションを起動")
    print("   ./run.sh")
    print("   または")
    print("   ar-uploader  (エイリアス設定時)")
    print()
    print("📚 詳細はドキュメントを参照:")
    print("   - README.md - 概要")
    print("   - README_macOS.md - macOS詳細ガイド")
    print()
    print("🌐 ブラウザでアクセス:")
    print("   http://localhost:5000")
    print()

def main():
    """Main setup process"""
    print_header("🎨 AR Model Uploader - Quick Start Setup")
    
    # Check system
    if not check_python():
        return False
    
    print()
    
    # Create venv
    if not create_venv():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Setup .env
    if not setup_env_file():
        return False
    
    # Create run script
    if not create_run_script():
        return False
    
    # Check credentials
    print()
    credentials_ok = check_credentials()
    
    # Create alias
    print()
    create_alias()
    
    # Show next steps
    show_next_steps()
    
    if not credentials_ok:
        print_warning("credentials.json がまだ設定されていません")
        print_info("設定後、アプリケーションを起動してください")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
