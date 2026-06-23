# 🚀 クイックスタートガイド

## 5分で始める AR Model Uploader

このガイドは、macOS で AR Model Uploader を最速でセットアップして動作させるための手順です。

---

## 📋 必要なもの

- ✅ macOS 10.15 以上
- ✅ インターネット接続
- ✅ Google アカウント

---

## ⚡ 1分セットアップ

### ステップ 1: リポジトリをクローン

```bash
git clone https://github.com/wintermute-HC/ar-model-uploader.git
cd ar-model-uploader
```

### ステップ 2: クイックスタートスクリプトを実行

```bash
python3 quickstart.py
```

**これで準備完了！** ☕ コーヒーを飲んで数分待つだけです。

---

## 🔐 3分で Google 認証設定

### ステップ 1: Google Cloud Console にアクセス

👉 https://console.cloud.google.com/

### ステップ 2: 新規プロジェクトを作成

1. 右上の **プロジェクト選択** をクリック
2. **新規プロジェクト** をクリック
3. プロジェクト名: `ar-model-uploader` と入力
4. **作成** をクリック

### ステップ 3: Google Drive API を有効化

1. 左メニューから **API とサービス** → **ライブラリ** をクリック
2. 検索ボックスに `Google Drive API` と入力
3. 検索結果をクリック
4. **有効にする** をクリック

### ステップ 4: サービスアカウントキーを生成

1. 左メニューから **API とサービス** → **認証情報** をクリック
2. **認証情報を作成** → **サービスアカウント** をクリック
3. 入力項目を埋める:
   - サービスアカウント名: `ar-model-uploader`
   - その他はデフォルトで OK
4. **作成して続行** をクリック
5. ロール選択画面で **Editor** を選択
6. **続行** → **完了** をクリック

### ステップ 5: JSON キーをダウンロード

1. 作成したサービスアカウントをクリック（一覧に表示）
2. **キー** タブをクリック
3. **キーを追加** → **新しいキーを作成** をクリック
4. **JSON** を選択して **作成** をクリック
5. JSONファイルが自動ダウンロードされます

### ステップ 6: credentials.json を配置

```bash
# ダウンロードしたファイルをプロジェクトディレクトリにコピー
cp ~/Downloads/*.json ./credentials.json
```

**完了！** 🎉

---

## 🎮 起動方法

### 方法 A: スクリプトで起動（推奨）

```bash
./run.sh
```

### 方法 B: 直接起動

```bash
source venv/bin/activate
python3 macos_app.py
```

### 方法 C: エイリアスで起動（簡単）

```bash
ar-uploader
```

**アプリケーションウィンドウが起動します！** 🎨

---

## 📱 使ってみよう

### 1. ファイルをアップロード

1. **📤 アップロード** タブを選択
2. **ファイルを選択** をクリック（またはドラッグ&ドロップ）
3. USDZ または GLB ファイルを選択
4. **モデルタイトル** を入力
5. **🚀 アップロード** をクリック

**✅ 完了！** Google Drive に自動的にアップロードされます。

### 2. AR で確認

1. **🎮 ビューアー** タブを選択
2. モデルを選択
3. 3D ビューアーにモデルが表示されます
4. マウスでドラッグして回転

**PC で AR が見られます！**

### 3. Google Sites に埋め込み

1. アップロード後、表示される **埋め込みコード** をコピー
2. [Google Sites](https://sites.google.com/) を開く
3. Webサイトを編集
4. **挿入** → **埋め込み** → **URLから埋め込む**
5. コピーしたコードを貼り付け
6. **次へ** → **挿入** をクリック

**完了！** Webサイトに AR が表示されます！

---

## 📱 実機で AR を見る

### iOS (iPhone/iPad)

1. Safariで Webサイトを開く
2. AR モデルで **📱 AR で見る** をタップ
3. AR Quick Look が起動
4. 周囲をスキャンして AR で表示

### Android

1. Chrome で Webサイトを開く
2. **📱 AR で見る** をタップ
3. AR が起動
4. デバイスをかざして表示

---

## 🔧 よくあるトラブル

### Q1: `credentials.json not found`

**A:** Google Cloud から credentials.json をダウンロードしてプロジェクトルートに配置してください

```bash
cp ~/Downloads/[downloaded].json ./credentials.json
```

### Q2: ポートが使用中

**A:** .env ファイルで PORT を変更してください

```bash
nano .env
# PORT=5001 に変更
```

### Q3: PyQt6 エラー

**A:** PyQt6 を再インストール

```bash
source venv/bin/activate
pip install --upgrade PyQt6 PyQt6-WebEngine
```

### Q4: Python モジュール not found

**A:** 仮想環境を有効化してください

```bash
source venv/bin/activate
```

---

## 📚 詳細ドキュメント

- **README.md** - プロジェクト概要
- **README_macOS.md** - macOS 詳細ガイド
- [Google Drive API Docs](https://developers.google.com/drive)
- [Model Viewer Docs](https://modelviewer.dev/)

---

## 💡 ヒント

### ファイル形式の選択

| 形式 | iOS | Android | PC | サイズ |
|------|-----|---------|----|----|
| GLB  | ⚠️ | ✅ | ✅ | 小 |
| USDZ | ✅ | ❌ | ⚠️ | 中 |

**両方に対応させたい？** → GLB をメインで使用。iOS は AR Quick Look で USDZ も提供

### ファイルサイズを減らす

```bash
# GLB ファイルを Blender で圧縮（推奨）
# 1. Blender で開く
# 2. File > Export > glTF 2.0 (.glb/.gltf)
# 3. Format: glTF Binary (.glb)
# 4. Export
```

### 複数ファイルを一度にアップロード

現在のバージョンでは1つずつですが、将来アップデートで対応予定です。

---

## 🎓 次のステップ

### 機能を活用する

- ✅ 複数モデルを管理
- ✅ カスタム埋め込みコードを生成
- ✅ AR 体験を共有

### カスタマイズ

- 🎨 UI をカスタマイズ
- 📱 独自のブランディング
- 🔒 認証機構を追加

### デプロイ

- 🚀 クラウドにデプロイ
- 🌐 独自ドメインで公開
- 📊 アナリティクスを追加

---

## 🆘 サポート

問題が発生しましたか？

1. **検索:** [Issues ページ](https://github.com/wintermute-HC/ar-model-uploader/issues) で検索
2. **質問:** 解決しない場合は新規 Issue を作成
3. **詳細:** エラーメッセージ＆スクリーンショットを添付

---

## ✨ 成功例

こんなことができます：

- 🛍️ **Eコマースサイト** - 商品を AR で確認
- 🏛️ **美術館・博物館** - 展示物を AR で体験
- 🎓 **教育** - 3D モデルで学習
- 🏢 **建築・不動産** - ビル・物件を AR で閲覧
- 🎮 **ゲーム** - キャラクターを AR で表示
- 📦 **製造業** - 製品を AR でデモ

---

## 📝 チェックリスト

セットアップ完了の確認：

- [ ] Python3 がインストール済み
- [ ] リポジトリをクローン
- [ ] quickstart.py を実行
- [ ] credentials.json を配置
- [ ] ./run.sh で起動
- [ ] ブラウザでアプリが表示
- [ ] テストファイルをアップロード
- [ ] AR でプレビュー確認

全てチェックできたら、あなたも AR の世界へ！ 🎉

---

## 🎯 まとめ

```
1. git clone
2. python3 quickstart.py
3. credentials.json を設定
4. ./run.sh
5. ファイルをアップロード
6. AR で楽しむ！
```

**簡単です！** 始めましょう🚀

---

**バージョン:** 1.0.0  
**最終更新:** 2026年6月23日  
**対応OS:** macOS 10.15+
