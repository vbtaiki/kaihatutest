# BOOKROAD 引き継ぎ情報

## リポジトリ
- GitHub: https://github.com/vbtaiki/bookroad
- ブランチ: master（メイン。すべてマージ済み）
- 本番URL: https://bookroad-kappa.vercel.app

## プロジェクト概要
BOOKROADは「本と旅する」をテーマにした読書体験アプリ。
本の登録、読書ステータス管理、本棚整理、読書ノート、AIエージェントとの対話ができる。

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
public.book_records     - 読書メモ（user_book_id, type[thought/quote], content, page, is_public）
public.shelves          - 本棚（user_id, name, color, description）
public.shelf_books      - 本棚×本（shelf_id, book_id）
public.journal_entries  - 読書日記（user_id, title, content, related_book_ids, is_public）
public.chat_messages    - チャット履歴
```

## ディレクトリ構成
```
app/                    - Next.js App Router
  app/api/              - APIルート
    books/              - 本のCRUD、検索、一括検索
    shelves/            - 本棚のCRUD、AI分析
    book-records/       - 読書記録（感想、引用）
    user-books/         - ユーザー×本の紐付け
    chat/               - AIチャット（私のAI）
    agents/             - エージェント（discover, chat）
    ai/                 - AI機能（book-analysis, home-insight, etc.）
    profile/            - ユーザープロフィール
    journal/            - 読書日記
    test-key/           - APIキー動作確認用（デバッグ用）
  app/login/            - ログイン画面
  app/auth/callback/    - 認証コールバック
components/bookroad/    - 画面コンポーネント
  home-screen.tsx       - ホーム画面
  search-screen.tsx     - 検索・一括取込画面
  bookshelf-screen.tsx  - 本棚画面
  book-detail-screen.tsx - 本の詳細画面
  agents-screen.tsx     - エージェント画面（招く・私の空間）
  ai-interview-screen.tsx - 私のAIチャット画面
hooks/use-api.ts        - API呼び出しフック
lib/
  supabase/             - Supabaseクライアント（client.ts, server.ts, middleware.ts）
  influencer-book-data.ts - インフルエンサーの本データ（ハードコード版、DB版と重複あり）
types/index.ts          - TypeScript型定義
supabase/               - DBマイグレーション
docs/                   - プロジェクトドキュメント（philosophy, strategy, concept等）
scripts/
  seed-agents.ts        - エージェント一括登録スクリプト
  agents/               - エージェントデータ定義
    types.ts            - 型定義
    index.ts            - 全エージェント統合
    influencers.ts      - ゆる言語学ラジオ、積読チャンネル
    authors.ts          - 村上春樹、岸見一郎
    historical.ts       - 夏目漱石、手塚治虫、アインシュタイン、クレオパトラ、ダ・ヴィンチ
    fictional.ts        - シャーロック・ホームズ、アン・シャーリー、ルフィ
    academics.ts        - 中野知恵（架空）、森田健二（架空）
```

## 実装済みの主要機能
- ログイン・認証（Supabase Auth、メール認証）
- 本の検索・登録（NDL国会図書館 + OpenBD API）
- CSV/テキストからの一括取込（30件ずつ分割送信、ISBN-10→13変換対応）
- 読書ステータス管理（読みたい/読書中/読了）
- 本棚の作成・整理
- 読書ノート（感想・引用の記録）
- AIチャット「私のAI」（ユーザーの本棚100冊をコンテキストに含む）
- エージェント「空間に招く」（他ユーザー or インフルエンサーのAIと対話）
- 本の詳細ページ（書影フォールバック、著者名フォーマット、AI分析「みんなの声」）
- ホーム画面のAIインサイト

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
# 全エージェントを再登録（既存ユーザーは検出して更新）
SUPABASE_URL=https://dmyqedkfaibrgqjhvwdk.supabase.co \
SUPABASE_SERVICE_ROLE_KEY="<service_roleキー>" \
npx tsx scripts/seed-agents.ts

# カテゴリ指定で一部だけ登録
npx tsx scripts/seed-agents.ts --filter influencer
```

## 直近の変更履歴（2026年3月）
```
c31ca24 feat: シードスクリプトをservice_role管理者APIに対応
e94fca3 fix: 私のAIチャットにユーザーの本棚データ（最大100冊）を渡すよう修正
d6a8fe1 fix: AIモデルをclaude-sonnet-4に戻す（claude-3-5-sonnetは廃止済み）
5b5e2d6 fix: APIエラー詳細をレスポンスに含めるよう改善・agents/discoverの安定化
9f72230 fix: ISBN-10→13変換時のMap参照キー不一致を修正
12a6937 fix: AIチャットエラー表示改善・一括取込上限撤廃・インフルエンサーエージェント追加
1e8fe4b fix: 書影フォールバック・著者名/発行年フォーマット改善・分析エラーハンドリング
```

## 残りの課題・改善ポイント

### 高優先度
- [ ] CSV一括取込のISBN検索が0件になる問題の調査（デバッグログ追加済み、Vercel Logsで確認）
- [ ] デバッグ用コード（console.log、test-keyエンドポイント）の削除（本番安定後に）
- [ ] `lib/influencer-book-data.ts` のハードコード版とDB版の重複整理（DB版で統一すべき）

### 中優先度
- [ ] デスクトップ表示の最適化（現在モバイル幅固定、PC幅で余白が大きい）
- [ ] 「探す」タブ下部のチャットUIの役割を明確にする
- [ ] エージェントのアバター画像の用意と設定（現在は空文字）

### 低優先度
- [ ] 読書日記（journal）機能の充実
- [ ] 本棚のおすすめ機能の強化
- [ ] 認証フローの改善（パスワードリセット等）
- [ ] middleware.ts → proxy への移行（Next.js 16の警告対応）
- [ ] エージェントの追加（新しいキャラクター、一般ユーザー型エージェント等）

## コマンド
```bash
pnpm install    # 依存関係インストール
pnpm dev        # 開発サーバー起動（http://localhost:3000）
pnpm build      # ビルド
pnpm lint       # リント
```

## 注意事項
- AIモデルは `claude-sonnet-4-20250514` を使用（`claude-3-5-sonnet-20241022` は廃止済み）
- Anthropic APIキーは Anthropic Console で $100クレジットがあるワークスペースから作成すること
- Vercelの環境変数を変更した後は必ず Redeploy が必要
- APIキーの動作確認: https://bookroad-kappa.vercel.app/api/test-key
- user_profilesテーブルは手動でSQL作成済み（マイグレーションファイルなし。CREATE TABLE文はCursorチャット履歴参照）
- エージェントのメールアドレスは全て `@bookroad-agent.com`、パスワードは `BookRoad2024!`
