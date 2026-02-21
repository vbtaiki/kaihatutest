# 🚀 Dashboard v2 クイックスタート

**5分で始める新しいダッシュボード**

---

## ステップ1: ダッシュボードを開く

### 方法A: ローカルサーバーで開く（推奨）

```bash
cd dashboard-v2
python3 -m http.server 8888
```

ブラウザで開く:
```
http://localhost:8888
```

### 方法B: 直接HTMLファイルを開く

`dashboard-v2/index.html` をダブルクリック

---

## ステップ2: 自分のチームを選択

右上のドロップダウンから自分のチームを選択すると、詳細が表示されます。

---

## ステップ3: データを更新する

### 3-1. Markdownを編集

通常通り、Cursorで組織図のMarkdownを更新します。

例:
```
「倉庫チームのミッションを更新して」
```

### 3-2. ビルドスクリプトを実行

プロジェクトのルートディレクトリで:

```bash
python3 build_dashboard.py
```

### 3-3. ブラウザをリロード

ダッシュボードをリロード（F5 / Cmd+R）すると、最新データが表示されます。

---

## 🎯 使い分け

| ユースケース | 使うべきもの |
|--------------|--------------|
| **組織図の更新** | Markdownファイル（teams/, members/） |
| **ダッシュボードの閲覧** | dashboard-v2/index.html |
| **データの同期** | build_dashboard.py |

---

## 💡 ワンライナー

Markdown更新からダッシュボード表示まで:

```bash
# 1. ビルド
python3 build_dashboard.py

# 2. サーバー起動
cd dashboard-v2 && python3 -m http.server 8888

# 3. ブラウザで開く（自動）
open http://localhost:8888
```

---

## 🔗 次のステップ

- 詳細な使い方: [README.md](README.md)
- 自動化の設定: [GitHub Actions設定](README.md#github-actionsで自動ビルド)
- デザインのカスタマイズ: [index.html](index.html)の`<style>`タグを編集

---

**Have fun! 📊**
