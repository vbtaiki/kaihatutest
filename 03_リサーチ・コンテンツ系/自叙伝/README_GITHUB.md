# GitHubで管理する - バリューブックス創業記

**このプロジェクトをGitHubで管理する方法**

---

## 🎯 GitHubで管理するメリット

### 1. バージョン管理
- ✅ すべての変更履歴が残る
- ✅ いつでも過去の状態に戻せる
- ✅ 「あの時の文章、やっぱり良かった」を復元できる

### 2. バックアップ
- ✅ クラウドに自動バックアップ
- ✅ PCが壊れても安心
- ✅ 複数デバイスで作業可能

### 3. 執筆の記録
- ✅ いつ、何を書いたかが分かる
- ✅ 執筆の軌跡が可視化される
- ✅ コミットメッセージで日記的に記録できる

### 4. 協力者との共有（オプション）
- ✅ 編集者やベータリーダーと共有できる
- ✅ フィードバックを受けやすい

---

## 🚀 初回セットアップ（ターミナルで実行）

### ステップ1: Gitの初期化

プロジェクトフォルダで以下を実行：

```bash
cd /Users/nakamurataiki/Desktop/自叙伝

# Gitの初期化
git init

# ユーザー情報の設定（まだの場合）
git config user.name "Nakamura Taiki"
git config user.email "your-email@example.com"

# 全てのファイルをステージング
git add .

# 初回コミット
git commit -m "🎉 執筆プロジェクト開始

- 序章〜第5章の初稿完成（13,000字）
- 執筆環境の構築完了（8つのドキュメント）
- システム開発 × 編集者のハイブリッドアプローチ"
```

### ステップ2: GitHubリポジトリの作成

1. **GitHubにログイン**
   - https://github.com

2. **新しいリポジトリを作成**
   - 「New repository」をクリック
   - Repository name: `valuebooks-autobiography`
   - Description: `バリューブックス創業記 - 執筆プロジェクト`
   - **Private** を選択（重要！）
   - 「Create repository」をクリック

3. **ローカルとリモートを連携**

```bash
# リモートリポジトリを追加
git remote add origin https://github.com/your-username/valuebooks-autobiography.git

# メインブランチの名前を変更（必要に応じて）
git branch -M main

# 初回プッシュ
git push -u origin main
```

---

## 📝 日々の執筆フロー

### 基本的なワークフロー

```bash
# 1. 今日の執筆を開始する前に、最新を取得
git pull

# 2. 執筆する

# 3. 変更をステージング
git add .

# 4. コミット（その日書いたことを記録）
git commit -m "📝 第6章：部屋の限界 執筆開始（1,200字追加）"

# 5. GitHubにプッシュ（バックアップ）
git push
```

### コミットメッセージの例

**執筆時:**
```bash
git commit -m "📝 第6章完成（3,000字）

- 部屋が本で埋まる様子を描写
- 生活空間がなくなる葛藤
- 初めて捨てることを考える瞬間"
```

**推敲時:**
```bash
git commit -m "✏️ 序章〜第1章の推敲

- 序章と第1章の繋ぎを改善
- 第1章の就活の描写を膨らませる
- 文体の統一"
```

**設計変更時:**
```bash
git commit -m "🎨 構成変更：第二部の章立てを調整

- 第8章と第9章を統合
- 新しく第10章を追加
- 全体のバランスを改善"
```

**マイルストーン:**
```bash
git commit -m "🎉 Phase 2 完了（第6-9章、25,000字）

- 第二部「拡大と痛み」完成
- 累計38,000字（目標の47%）
- 次は第10章から"
```

---

## 🌿 ブランチ戦略（オプション）

### シンプル戦略（推奨）

```
main
 └── すべての執筆をここで行う
```

メリット:
- シンプル
- 一人での執筆に最適
- 混乱しない

### 発展的な戦略

```
main (安定版)
 ├── draft (執筆中)
 ├── revision (推敲中)
 └── experiment (実験的な書き直し)
```

使い方:
```bash
# 新しい章を書く時
git checkout -b draft/chapter-06
# 書き終えたら
git checkout main
git merge draft/chapter-06

# 推敲する時
git checkout -b revision/phase-1
# 推敲し終えたら
git checkout main
git merge revision/phase-1
```

---

## 📊 執筆の可視化

### GitHub上で見られる情報

1. **コミット履歴**
   - いつ、何を書いたか
   - 執筆のペース

2. **差分表示**
   - 何が変わったか
   - 削除した文章、追加した文章

3. **統計情報**
   - 総コミット数
   - 追加・削除した行数

4. **グラフ**
   - 執筆の推移
   - アクティビティ

---

## 🔒 プライバシーとセキュリティ

### 必ずプライベートリポジトリに

- ✅ **Private** を選択する
- ❌ **Public** にしない（原稿が公開される）

### 注意すべきこと

1. **個人情報**
   - 実名、住所、電話番号などは書かない
   - または `.gitignore` で除外

2. **機密情報**
   - 売上、給与などの具体的数字
   - 公開したくない人名
   - これらは別ファイルにして `.gitignore`

3. **出版前の原稿**
   - 出版社と契約したら、公開範囲を確認
   - 必要なら、一時的にプライベート化

---

## 🛠️ 便利なGitコマンド

### 状態確認
```bash
# 変更されたファイルを確認
git status

# 変更内容を確認
git diff

# コミット履歴を確認
git log --oneline
```

### 間違えた時
```bash
# 直前のコミットを取り消す（変更は残る）
git reset HEAD~1

# 特定のファイルの変更を取り消す
git checkout -- ファイル名

# 特定のコミットに戻る
git revert コミットID
```

### 過去の文章を見る
```bash
# 特定の日付のファイルを見る
git show HEAD~3:序章_本の還る場所.md

# 特定のコミットのファイルを復元
git checkout コミットID -- ファイル名
```

---

## 📅 定期的なメンテナンス

### 毎日
```bash
git add .
git commit -m "📝 今日の執筆内容"
git push
```

### 毎週
```bash
# タグをつけてマイルストーンを記録
git tag -a v0.1.0 -m "Week 1: 第6章完成"
git push --tags
```

### Phase完了時
```bash
git tag -a phase-2-complete -m "Phase 2 完了（第6-9章）"
git push --tags
```

---

## 🎯 GitHubのIssues活用（オプション）

### Issuesをタスク管理に使う

例:
```markdown
# Issue #1: 第6章「部屋の限界」を書く

## やること
- [ ] エピソード収集
- [ ] 構成決定
- [ ] 初稿執筆（3,000字）
- [ ] 推敲

## 締切
2026年1月9日

## メモ
- 生活空間がなくなる様子を丁寧に
- 初めて「捨てる」ことを考える葛藤
```

---

## 🤝 協力者との共有（オプション）

### ベータリーダーや編集者と共有する場合

1. **Collaboratorとして招待**
   - Settings > Collaborators
   - 相手のGitHubアカウントを追加

2. **Pull Requestでフィードバック**
   - 協力者がコメントを残せる
   - 修正提案を受けられる

---

## ⚠️ トラブルシューティング

### Q: プッシュできない
```bash
# 強制的に最新を取得
git pull --rebase origin main
git push
```

### Q: コンフリクトが起きた
```bash
# 手動で修正してから
git add .
git commit -m "コンフリクト解決"
git push
```

### Q: 間違えてコミットした
```bash
# 直前のコミットを修正
git commit --amend -m "正しいメッセージ"
git push --force
```

---

## 📚 参考リンク

- [Git公式ドキュメント](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com/ja)
- [Git入門（日本語）](https://backlog.com/ja/git-tutorial/)

---

## ✅ セットアップチェックリスト

執筆を始める前に確認：

- [ ] Gitがインストールされている（`git --version` で確認）
- [ ] GitHubアカウントがある
- [ ] `git init` を実行した
- [ ] `.gitignore` が作成されている
- [ ] 初回コミットをした
- [ ] GitHubにプライベートリポジトリを作成した
- [ ] リモートとローカルを連携した（`git remote -v` で確認）
- [ ] 初回プッシュが成功した

---

**Remember:** コミットは小さく、頻繁に。書いた直後にコミット、一日の終わりにプッシュ。

