#!/bin/bash
# ===================================
# 本棚スキャン プロジェクトサイトをGitHub Pagesで公開するスクリプト
# 使い方: bash publish.sh
# ===================================

set -e

echo "📚 本棚スキャン プロジェクトサイトの公開を開始します..."

cd /Users/nakamurataiki/Desktop
if [ -d "hondanascan" ]; then
    echo "既存のフォルダを更新します..."
    cd hondanascan
    git pull
else
    echo "リポジトリを取得しています..."
    git clone https://github.com/vbtaiki/hondanascan.git
    cd hondanascan
fi

mkdir -p docs
cp /Users/nakamurataiki/Desktop/CURSOR/projects/画像認識本棚スキャン/demo/index.html docs/index.html

echo "✅ サイトファイルを配置しました"

git add -A
git commit -m "[biz] プロジェクトサイトを更新" || echo "変更なし"
git push

echo ""
echo "✅ 公開完了！"
echo "🌐 https://vbtaiki.github.io/hondanascan/"
