# BOOKROAD 引き継ぎ情報

最終更新: 2026年3月25日

## リポジトリ
- GitHub: https://github.com/vbtaiki/bookroad
- ブランチ: master（メイン。すべてマージ済み）
- 本番URL: https://bookroad-kappa.vercel.app
- 作業ディレクトリ: `/Users/nakamurataiki/Desktop/CURSOR/.tmp-bookroad-debug/bookroad`

## プロジェクト概要
BOOKROADは「本と旅する」をテーマにした読書体験アプリ。
本の登録、読書ステータス管理、テーマ棚整理、読書ノート、AIエージェントとの対話ができる。

## 技術スタック
- フロントエンド: Next.js 16 (App Router), TypeScript, Tailwind CSS, Radix UI (shadcn/ui)
- バックエンド: Supabase (PostgreSQL, Auth, Storage)
- AI: Anthropic Claude API (`claude-sonnet-4-20250514`)
- ホスティング: Vercel
- パッケージ管理: pnpm

## 環境変数（Vercelに設定済み）
- `NEXT_PUBLIC_SUPABASE_URL` — SupabaseプロジェクトのURL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` — Supabaseの匿名キー
- `ANTHROPIC_API_KEY` — Anthropic APIキー（`sk-ant-api03-...` 形式）
- `ADMIN_SECRET` — フィードバック管理API用シークレット（設定必須）

## Supabase情報
- プロジェクトref: `dmyqedkfaibrgqjhvwdk`
- URL: `https://dmyqedkfaibrgqjhvwdk.supabase.co`
- service_roleキーはSupabase Dashboard → Settings → API → Legacy タブから取得

## DBテーブル構成
```
auth.users              - ユーザー認証（Supabase Auth管理）
public.user_profiles    - プロフィール（display_name, bio, agent_type, tags, is_agent_public）
public.books            - 本マスタ（title, author, publisher, year, pages, isbn, cover_url）
public.user_books       - ユーザー×本（user_id, book_id, status, liked, is_public, progress）
                          status: want-to-read / tsundoku / reading / on-hold / finished
public.book_records     - 読書メモ（user_book_id, type[thought/quote], content, page, is_public）
public.shelves          - テーマ棚（user_id, name, color, description）
public.shelf_books      - テーマ棚×本（shelf_id, book_id）
public.journal_entries  - 読書日記（user_id, title, content, related_book_ids, is_public）
public.chat_messages    - チャット履歴
public.feedback         - ユーザーフィードバック（以下参照）
public.site_overrides   - AIが自動適用したUI修正の記録
```

### feedback テーブル（詳細）
```
id                  UUID PRIMARY KEY
user_id             UUID（ログイン中ユーザー）
page                TEXT（フィードバック送信時のページ名）
content             TEXT（フィードバック本文）
user_agent          TEXT
screenshot_urls     TEXT[]（Supabase Storageの公開URL一覧）
page_context        JSONB（送信時の画面コンテキスト自動収集データ）
status              TEXT: pending / auto_fixed / reviewed / dismissed / on_hold
ai_verdict          TEXT: auto_fix / needs_review / invalid
ai_reasoning        TEXT（AI判定理由）
ai_fix_description  JSONB（AI修正詳細）
owner_note          TEXT（開発者メモ）
created_at          TIMESTAMPTZ
reviewed_at         TIMESTAMPTZ
```

### Supabase Storage バケット
```
feedback-screenshots  - フィードバック添付スクリーンショット（公開読み取り）
                        最大5MB/枚、jpeg/png/webp/gif 対応
```

## ディレクトリ構成
```
app/                    - Next.js App Router
  app/api/
    books/              - 本のCRUD、検索、一括検索（NDL+OpenBD）
    shelves/            - テーマ棚のCRUD、AI分析
    book-records/       - 読書記録（感想、引用）
    user-books/         - ユーザー×本の紐付け
    chat/               - AIチャット（私のAI）
    agents/             - エージェント（discover, chat）
    ai/                 - AI機能（book-analysis, home-insight, quick-tags等）
    profile/            - ユーザープロフィール
    journal/            - 読書日記
    feedback/           - フィードバック投稿・取得・ステータス更新
    admin/
      feedback-summary/ - AI参照用フィードバック一覧API（ADMIN_SECRET保護）
    import-chat/        - 画像・ファイルからの本取り込み
    site-overrides/     - AIが適用したUI修正の取得
  app/login/            - ログイン・サインアップ画面
  app/auth/callback/    - 認証コールバック（メール確認後のセッション確立）
components/bookroad/
  home-screen.tsx         - ホーム画面（ライブラリ）
  dashboard-screen.tsx    - ダッシュボード（クイック評価・発見・統計）
  search-screen.tsx       - 検索・取り込み画面
  book-discover-screen.tsx - 本を発見する（フルスクリーン版）
  bookshelf-screen.tsx    - テーマ棚管理画面
  book-detail-screen.tsx  - 本の詳細・ステータス変更
  my-books-screen.tsx     - ライブラリ一覧・フィルター
  agents-screen.tsx       - エージェント画面
  ai-interview-screen.tsx - 私のAIチャット
  feedback-widget.tsx     - フィードバックウィジェット（画面右下FAB）
hooks/use-api.ts          - API呼び出しフック
lib/
  supabase/               - Supabaseクライアント（client.ts, server.ts, middleware.ts）
  api-utils.ts            - Anthropicエラーハンドリング（日本語化）
  influencer-book-data.ts - インフルエンサーの本データ（ハードコード版。DB版と重複あり）
supabase/migrations/      - DBマイグレーションSQL
scripts/
  seed-agents.ts          - エージェント一括登録スクリプト
  agents/                 - エージェントデータ定義（influencers/authors/historical/fictional/academics）
```

## 実装済みの主要機能

### 本の管理
- ログイン・認証（Supabase Auth、メール認証）
- 本の検索・登録（NDL国会図書館 + OpenBD API）
- CSV/テキスト/画像/URLからの一括取込（マルチモーダル対応）
- 読書ステータス管理（**5段階**: 読みたい / 積読中 / 読書中 / 途中 / 読了）
- テーマ棚の作成・整理（ユーザー作成のテーマ別コレクション）
- 読書ノート（感想・引用の記録）

### AI機能
- AIチャット「私のAI」（ユーザーの本棚最大100冊をコンテキストに含む）
- エージェント（他ユーザー or インフルエンサーのAIと対話）
- 本の詳細ページ（AI分析「みんなの声」）
- ホーム画面のAIインサイト
- クイック評価タグのAI自動生成

### 本を発見する
- フルスクリーン版（`book-discover-screen.tsx`）とダッシュボード埋め込み版の2種類
- 初回起動時にオンボーディングアンケート（ジャンル選択→ムード選択 2ステップ）
- 選択内容をlocalStorageに保存し、以後の推薦に反映
- ボタンは「パス」「読みたい！」の明確な2択
- パスした本はlocalStorageで記憶（再表示なし）

### フィードバック収集
- 画面右下のFABボタンから送信
- **自動収集**: html2canvasでページスクリーンショット自動撮影（バックグラウンド）
- **自動収集**: デバイス種別・ビューポート・スクロール位置・通信状況・見えていた要素
- **手動添付**: 最大3枚まで画像を添付可能（自動圧縮）
- Anthropicに画像ごと渡してAIが判定（auto_fix / needs_review / invalid）
- 軽微な修正はAIが自動適用（site_overrides テーブル経由）

### フィードバック管理（AI参照用）
```
GET /api/admin/feedback-summary?secret=ADMIN_SECRET
```
- ステータス別グループ（未対応/保留/自動修正済み/対応済み/対応しない）
- ページ別件数サマリー
- 各フィードバックの内容・AI判定・スクリーンショット数・コンテキスト情報を整形
- AIアシスタントがいつでも参照して会話中に把握できるよう設計

ステータス変更:
```
PATCH /api/feedback
body: { id, status: "reviewed"|"dismissed"|"on_hold"|"pending", owner_note }
```

## 命名規則（UI上の表示名）
| 概念 | UI表示 | 説明 |
|---|---|---|
| 全本コレクション | **ライブラリ** | ユーザーが登録した全本（仕分け前） |
| テーマ別棚 | **テーマ棚** | ユーザーが作成する任意のテーマ別コレクション |
| ボトムナビ「ライブラリ」 | ライブラリ | 旧「本棚」から変更済み |

## 登録済み公式エージェント（14アカウント）
2026年3月にシードスクリプトで一括登録。合計111冊・129メモ・24本棚・15ジャーナル。

| カテゴリ | エージェント名 | タイプ | 本の数 |
|---------|-------------|-------|-------|
| インフルエンサー | ゆる言語学ラジオ | ポッドキャスター | 12冊 |
| インフルエンサー | 積読チャンネル | YouTuber | 12冊 |
| 作家 | 村上春樹 | 作家 | 10冊 |
| 作家 | 岸見一郎 | 哲学者 | 10冊 |
| 歴史 | 夏目漱石 | 文豪 | 8冊 |
| 歴史 | 手塚治虫 | 漫画家 | 8冊 |
| 歴史 | アインシュタイン | 物理学者 | 6冊 |
| 歴史 | クレオパトラ7世 | 女王・学者 | 5冊 |
| 歴史 | ダ・ヴィンチ | 万能の天才 | 5冊 |
| フィクション | シャーロック・ホームズ | 名探偵 | 6冊 |
| フィクション | アン・シャーリー | 夢見る少女 | 7冊 |
| フィクション | ルフィ | 海賊 | 6冊 |
| 学術 | 中野知恵（架空） | 認知科学者 | 8冊 |
| 学術 | 森田健二（架空） | 書評家 | 8冊 |

### エージェント再登録・追加方法
```bash
SUPABASE_URL=https://dmyqedkfaibrgqjhvwdk.supabase.co \
SUPABASE_SERVICE_ROLE_KEY="<service_roleキー>" \
npx tsx scripts/seed-agents.ts

# カテゴリ指定で一部だけ
npx tsx scripts/seed-agents.ts --filter influencer
```

## 直近の変更履歴（2026年3月）
```
a25a6bb feat: AI参照用フィードバック管理エンドポイント追加
3566e38 fix: マイグレーション未適用でもフォールバック動作するよう修正
75739e4 feat: フィードバック送信時に画面状況を自動収集（html2canvas + PageContext）
131491d feat: フィードバックにスクリーンショット添付機能を追加
a00f0be fix: ダッシュボードの発見ボタン2択化・本棚命名整理
d25cd1d feat: 本を発見する UX改善 + オンボーディングアンケート追加
e41de12 feat: 積読中・途中ステータス追加、ナレッジ→日本語化、ライブラリ/テーマ棚の命名整理
（以前）fix: ユーザーフィードバックバグ修正（認証フロー・画像認識・エラー表示等）
```

## 残りの課題・改善ポイント

### 対応中 / 保留
- [ ] `lib/influencer-book-data.ts` のハードコード版とDB版の重複整理
  - ハードコード版（4名分）を `agents/discover` と `agents/chat` が参照中
  - DB版に一本化が望ましいが、影響範囲が広い

### 未着手
- [ ] エージェントのアバター画像
  - シードデータに `/agents/*.jpg` のパスが定義されているが `public/agents/` に画像なし
  - `historical.ts`, `fictional.ts`, `academics.ts` は `avatarUrl: ""` のまま
  - フォールバック（グラデーション）は動作するが、見た目の差別化に課題
- [ ] パスワードリセット未実装（ログイン画面にリセットフローなし）
- [ ] 読書日記（journal）の編集UI・本の紐づけUI（APIは実装済み、画面側が不足）
- [ ] エージェントの追加（芸能人・書店員・出版社編集者など要望あり）
- [ ] 「つながりマップ」：本と本が線で繋がるビジュアライゼーション（ゆる言語学ラジオから要望）
- [ ] 「読書年表」：いつ何を読んだかの時系列表示（コテンラジオから要望）
- [ ] PWA対応（manifest.json エラーが出ている）

### 解決済み
- [x] 新規ユーザー登録後にエージェントが動かない → 認証コールバックのCookie設定修正
- [x] 未認証APIリクエストのサイレント失敗 → middleware.tsで401を返すよう修正
- [x] 画像インポート時の「user messages must have non-empty content」エラー → 空コンテンツフィルター追加
- [x] 画像認識精度の改善 → OCR削除、直接Anthropicビジョンに渡すよう変更
- [x] `api/test-key` セキュリティリスク → 削除済み
- [x] `api/site-overrides` 500エラー → テーブル未存在時に200+{}を返すよう修正
- [x] AIが評価を意図せず上書きする問題 → userExplicitRatingIntent をより厳格に
- [x] NDL検索でタイトル+著者が混在して精度が低い → creator= パラメータ分離
- [x] 積読中・途中ステータスがなかった → 5段階（want-to-read/tsundoku/reading/on-hold/finished）に拡張
- [x] 「ナレッジ」という言葉が分かりにくい → 「参照します」等の自然な日本語に置き換え
- [x] 本棚の命名が混乱 → ライブラリ（全本）/ テーマ棚（テーマ別）に整理

## コマンド
```bash
pnpm install    # 依存関係インストール
pnpm dev        # 開発サーバー起動（http://localhost:3000）
pnpm build      # ビルド
pnpm lint       # リント
```

## 注意事項
- AIモデルは `claude-sonnet-4-20250514` を使用
- `app/api/test-key/` は削除済み（セキュリティリスクのため）。注意事項から参照箇所も削除
- Vercelの環境変数を変更した後は必ず Redeploy が必要
- user_profilesテーブルは手動でSQL作成済み（マイグレーションファイルなし）
- エージェントのメールアドレスは全て `@bookroad-agent.com`、パスワードは `BookRoad2024!`
- フィードバック管理APIは `ADMIN_SECRET` 環境変数をVercelに設定しないと使えない

## Supabase マイグレーション適用状況
```
20260324_create_feedback.sql          ✅ 適用済み
20260325_feedback_screenshots.sql     ✅ 適用済み（screenshot_urls + Storageバケット）
20260325_feedback_page_context.sql    ✅ 適用済み（page_context JSONB）
20260325_feedback_on_hold_status.sql  ✅ 適用済み（on_holdステータス追加）
RUN_IN_DASHBOARD.sql                  - 上記を1ファイルにまとめたもの（再実行不要）
```
