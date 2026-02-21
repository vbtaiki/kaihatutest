# 🚀 バリューブックス デジタル経営コックピット

## スタートガイド

このディレクトリには、バリューブックスのデジタル改革を実現するための7つのプロジェクトが含まれています。
SaaSに依存せず、**Pythonだけ**であらゆる業務を自動化・最適化できる環境です。

---

## 📦 セットアップ（初回のみ）

### 1. Python環境の確認
```bash
python --version  # Python 3.9以上を推奨
```

### 2. 依存パッケージのインストール
```bash
cd valuebooks_lab
pip install -r requirements.txt
```

---

## 🎮 各プロジェクトの起動方法

### 📚 01_custom_crm（顧客管理システム）
**Salesforce代替の軽量CRM**

```bash
streamlit run 01_custom_crm/app.py
```
→ ブラウザで `http://localhost:8501` が自動で開きます

**機能:**
- 顧客検索（ID/氏名/ランク）
- 買取履歴・対応履歴の一覧表示
- 担当者メモの追加

---

### 👥 02_employee_evaluation（人事評価ツール）
**レーダーチャートでスキルを可視化**

```bash
open 02_employee_evaluation/index.html
# または、ブラウザで直接ファイルを開く
```

**機能:**
- 社員選択でスキル評価を表示
- 貢献係数・目標達成率の確認
- 定性評価コメントの閲覧

---

### 🤖 03_auto_reply_bot（メール自動返信ボット）
**n8n不要！Pythonで常駐自動化**

```bash
python 03_auto_reply_bot/bot.py
```

**機能:**
- ダミー受信トレイを10秒ごとに監視
- 問い合わせ内容をRAG（キーワードマッチング）で分析
- 適切な返信テンプレートを選択してログに保存

**停止方法:** `Ctrl + C`

---

### 💰 04_pricing_simulator（買取価格シミュレーター）
**利益率と回転率の最適解を探る**

```bash
python 04_pricing_simulator/simulator.py
```

**機能:**
- 過去の買取データに基づくシミュレーション
- ベース買取率の感度分析
- カテゴリ別の利益分析

---

### 🏭 05_warehouse_visualizer（倉庫AGVビジュアライザー）
**ロボットの動きをアニメーションで確認**

```bash
python 05_warehouse_visualizer/visualizer.py
```

**機能:**
- 50×50グリッドの倉庫レイアウト
- 3台のAGVがリアルタイムで移動
- 注文発生〜ピッキング〜出荷の流れを可視化

---

### ✍️ 06_writing_studio（執筆支援環境）
**経営哲学書の執筆ガイド**

以下のファイルをテキストエディタで開いてください：

- `06_writing_studio/style_guide.md` - 文体定義
- `06_writing_studio/draft_chapter1.md` - 第一章ドラフト

**スタイルガイドの特徴:**
- イヴォン・シュイナードの実践性
- レイチェル・カーソンの詩情
- H.D.ソローの哲学

---

### 📜 07_governance_constitution（憲法チェッカー）
**M&A・重要案件の承認プロセスを確認**

```bash
python 07_governance_constitution/checker.py
```

**機能:**
- 案件の決定レベル判定（A〜D）
- M&A選定基準のチェック
- 必要な承認プロセスの表示

**参照ドキュメント:**
- `07_governance_constitution/constitution.md` - 組織憲法

---

## 🗂 ディレクトリ構造

```
valuebooks_lab/
├── START_GUIDE.md          # ← このファイル
├── requirements.txt        # 依存パッケージ
│
├── 01_custom_crm/          # 顧客管理システム
│   ├── app.py              # Streamlitアプリ
│   ├── customers.csv       # 顧客マスタ
│   └── interactions.csv    # 対応履歴
│
├── 02_employee_evaluation/ # 人事評価ツール
│   ├── index.html          # ビューア
│   └── employees.json      # 社員データ
│
├── 03_auto_reply_bot/      # 自動返信ボット
│   ├── bot.py              # メインスクリプト
│   ├── inquiry_patterns.json  # 回答パターン
│   ├── dummy_inbox.json    # ダミー受信トレイ
│   └── reply_log.json      # 返信ログ（実行後に生成）
│
├── 04_pricing_simulator/   # 買取価格シミュレーター
│   ├── simulator.py        # シミュレーションスクリプト
│   └── historical_data.csv # 過去の買取データ
│
├── 05_warehouse_visualizer/ # 倉庫ビジュアライザー
│   └── visualizer.py       # アニメーションスクリプト
│
├── 06_writing_studio/      # 執筆支援
│   ├── style_guide.md      # 文体ガイド
│   └── draft_chapter1.md   # ドラフト原稿
│
└── 07_governance_constitution/ # ガバナンス
    ├── checker.py          # 憲法チェッカー
    └── constitution.md     # 組織憲法
```

---

## 💡 次のステップ

### おすすめの試用順序

1. **まず `03_auto_reply_bot` を起動**
   - n8nを使わない自動化の感覚を掴む
   - `reply_log.json` に返信案が蓄積されていく様子を確認

2. **次に `01_custom_crm` を起動**
   - Salesforceのような複雑なUIは不要
   - 本当に必要な情報だけが見える快適さを体感

3. **`04_pricing_simulator` で経営判断**
   - 係数を0.1変えるだけで粗利がどう変わるか
   - データに基づく意思決定の第一歩

### カスタマイズのヒント

- **ダミーデータを実データに置き換える**
  - CSVファイルを自社のデータで上書き
  - 列名を合わせるだけでOK

- **自動化ボットを本番稼働させる**
  - `bot.py` のメール取得部分を本物のIMAPに置き換え
  - AWSやGCPでスケジューリング実行

---

## 📞 サポート

このプロジェクトは、Cursorを使って構築されました。
追加の機能やカスタマイズが必要な場合は、Cursorに「〇〇を追加して」と指示するだけで拡張できます。

---

**Welcome to the Future of Valuebooks.** 📚✨



