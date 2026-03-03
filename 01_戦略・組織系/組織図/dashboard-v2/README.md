# Value Books OS Dashboard v2

**Markdownから自動生成される、常に最新のダッシュボード**

---

## 🎯 v2の特徴

### 従来版（dashboard/）との違い

| 項目 | 従来版 | v2（このバージョン） |
|------|--------|---------------------|
| **データ管理** | HTML内に直書き | Markdownから自動生成 |
| **更新方法** | HTMLを手動編集 | Markdownを更新 → ビルド |
| **信頼性** | 二重管理で破綻しやすい | Single Source of Truth |
| **リアルタイム性** | 手動更新が必要 | 自動で最新化 |
| **更新日時** | 手動で記入 | 自動で記録 |

---

## 📦 ファイル構成

```
dashboard-v2/
├── index.html          # ダッシュボード本体（動的データ読み込み）
├── data.json           # 自動生成されたデータ（編集不要）
└── README.md           # このファイル
```

---

## 🚀 使い方

### 1. Markdownファイルを更新

通常通り、Cursorで組織図のMarkdownファイルを更新します。

```
「倉庫チームのFounder's Expectationを更新したい」
→ teams/1-warehouse/README.md が更新される
```

### 2. ビルドスクリプトを実行

ルートディレクトリで以下を実行します。

```bash
python3 build_dashboard.py
```

**出力:**
```
🔨 VB-OS Dashboard Builder
📁 Root directory: .

📊 Building data from Markdown files...
✅ Found 6 teams
✅ Found 17 members

💾 Data saved to: dashboard-v2/data.json
📅 Updated at: 2026-01-19T13:15:10.556739

✨ Build complete!
```

### 3. ダッシュボードを開く

ブラウザで `dashboard-v2/index.html` を開きます。

```bash
# ローカルサーバーを起動（推奨）
cd dashboard-v2
python3 -m http.server 8888

# ブラウザで開く
open http://localhost:8888
```

または、HTMLファイルを直接ダブルクリックしても動作します。

---

## 💡 主な機能

### 1. Variable Resolution（解像度切り替え）

右上のセレクトボックスで自分のチームを選択すると：

- **自チーム**: 拡大表示 + Founder's Expectation + KPI + メンバー詳細
- **他チーム**: 縮小表示 + 概要のみ

![Variable Resolution](https://via.placeholder.com/800x400?text=Variable+Resolution+Demo)

### 2. リアルタイム統計

ヘッダーに「リアルタイム同期」インジケーターが表示され、データが最新であることを示します。

### 3. KPI可視化

各チームのKPIが「現状 → 目標」の形式で表示されます。

### 4. プロジェクトステータス

プロジェクトのステータスが色分けされて表示されます。

- 🟡 計画中（Planning）
- 🔵 進行中（Progress）
- 🟢 完了（Completed）

---

## 🔄 自動化の仕組み

```
teams/1-warehouse/README.md
    ↓
    | Markdownから情報を抽出:
    | - チーム名
    | - Founder's Expectation
    | - ミッション
    | - メンバー
    | - KPI
    | - プロジェクト
    ↓
dashboard-v2/data.json
    ↓
    | JavaScriptで動的に読み込み
    ↓
dashboard-v2/index.html (ブラウザで表示)
```

---

## 🛠️ カスタマイズ

### ビルドスクリプトの拡張

`build_dashboard.py` を編集することで、抽出するデータをカスタマイズできます。

例: プロジェクトの進捗率を追加

```python
# build_dashboard.py の _extract_projects() メソッドを編集

def _extract_projects(self, content: str) -> List[Dict[str, str]]:
    projects = []
    # ... 既存のコード ...

    # 進捗率を抽出
    progress_match = re.search(r'進捗: (\d+)%', details)
    if progress_match:
        project['progress'] = int(progress_match.group(1))

    projects.append(project)
    return projects
```

### デザインのカスタマイズ

`index.html` の `<style>` タグ内を編集してください。

カラーパレットは `:root` で定義されています。

```css
:root {
    --primary: #00BFA5;        /* メインカラー */
    --primary-light: #E0F7F4;  /* 背景色 */
    --text: #1A1A1A;           /* テキスト色 */
}
```

---

## 🚀 本番運用への展開

### GitHub Actionsで自動ビルド

`.github/workflows/build-dashboard.yml` を作成します。

```yaml
name: Build Dashboard

on:
  push:
    paths:
      - 'teams/**/*.md'
      - 'members/**/*.md'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Dashboard
        run: python3 build_dashboard.py
      - name: Commit changes
        run: |
          git config user.name "Dashboard Bot"
          git config user.email "bot@valuebooks.jp"
          git add dashboard-v2/data.json
          git commit -m "Update dashboard data [skip ci]" || exit 0
          git push
```

これで、Markdownを更新してpushすると、自動的にダッシュボードが更新されます。

### Vercelでホスティング

```bash
# Vercel CLIをインストール
npm i -g vercel

# デプロイ
cd dashboard-v2
vercel

# → https://vb-os-dashboard.vercel.app のようなURLが生成される
```

---

## 📊 データ構造

生成される `data.json` の構造：

```json
{
  "meta": {
    "updated_at": "2026-01-19T13:15:10.556739",
    "version": "1.0.0"
  },
  "teams": [
    {
      "id": "1-warehouse",
      "name": "倉庫 (Warehouse)",
      "icon": "🏭",
      "mission": "...",
      "expectation": "...",
      "members": [...],
      "kpis": [...],
      "projects": [...]
    }
  ],
  "members": [
    {
      "id": "hayashi",
      "name": "林",
      "role": "拠点責任者",
      "teams": [...],
      "projects": [...]
    }
  ]
}
```

---

## ❓ トラブルシューティング

### Q. ダッシュボードが真っ白になる

A. ブラウザの開発者ツール（F12）でコンソールを確認してください。`data.json`が見つからないエラーが出ている場合は、ローカルサーバーを起動してください。

```bash
cd dashboard-v2
python3 -m http.server 8888
```

### Q. データが古いまま更新されない

A. ブラウザのキャッシュをクリアしてください（Cmd+Shift+R / Ctrl+Shift+R）。

### Q. ビルドスクリプトでエラーが出る

A. Python 3.7以上が必要です。バージョンを確認してください。

```bash
python3 --version
```

---

## 🎯 今後の拡張予定

- [ ] メンバー詳細ページの追加
- [ ] プロジェクト詳細ページの追加
- [ ] 戦略文書ページとの連携
- [ ] KPIのグラフ表示
- [ ] 検索機能
- [ ] フィルター機能（チーム・ステータス別）

---

## 📝 メンテナンス

### データ更新の頻度

- **推奨**: Markdownを更新するたびにビルド
- **最低**: 週1回の定期ビルド

### バックアップ

`data.json` はGitで管理されるため、履歴が残ります。

---

*Last Updated: 2026-01-19*
