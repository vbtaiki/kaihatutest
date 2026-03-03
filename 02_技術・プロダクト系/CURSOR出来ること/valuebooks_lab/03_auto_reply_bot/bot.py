"""
バリューブックス 自動返信ボット
n8nを使わず、Pythonの常駐スクリプトで自動化を実現

使い方:
  python bot.py

停止方法:
  Ctrl+C
"""

import json
import time
import os
from datetime import datetime
from typing import Optional

# 設定
CHECK_INTERVAL = 10  # 秒（本番では60秒以上を推奨）
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
INBOX_FILE = os.path.join(DATA_DIR, 'dummy_inbox.json')
PATTERNS_FILE = os.path.join(DATA_DIR, 'inquiry_patterns.json')
LOG_FILE = os.path.join(DATA_DIR, 'reply_log.json')


def load_json(filepath: str) -> dict:
    """JSONファイルを読み込む"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath: str, data: dict) -> None:
    """JSONファイルに保存する"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def calculate_similarity(text: str, keywords: list) -> float:
    """
    簡易的なキーワードマッチングによる類似度計算
    本番ではベクトル検索（Embedding + コサイン類似度）を使用
    """
    if not keywords:
        return 0.0
    
    text_lower = text.lower()
    matches = sum(1 for kw in keywords if kw.lower() in text_lower)
    return matches / len(keywords)


def find_best_pattern(inquiry_text: str, patterns: list) -> dict:
    """
    問い合わせ内容に最もマッチするパターンを見つける
    
    RAG（Retrieval-Augmented Generation）の簡易実装:
    1. 問い合わせテキストを受け取る
    2. パターンDBから類似度が高いものを検索
    3. 該当テンプレートを返す
    """
    best_pattern = None
    best_score = 0.0
    
    for pattern in patterns:
        score = calculate_similarity(inquiry_text, pattern['keywords'])
        if score > best_score:
            best_score = score
            best_pattern = pattern
    
    # 類似度が低い場合は「その他」パターンを使用
    if best_score < 0.2:
        for pattern in patterns:
            if pattern['category'] == 'その他':
                return pattern
    
    return best_pattern if best_pattern else patterns[-1]


def generate_reply(email: dict, pattern: dict) -> dict:
    """返信を生成する"""
    return {
        'to': email['from'],
        'subject': f"Re: {email['subject']}",
        'body': pattern['answer_template'],
        'matched_category': pattern['category'],
        'original_email_id': email['id'],
        'generated_at': datetime.now().isoformat()
    }


def log_reply(reply: dict) -> None:
    """返信をログファイルに記録する"""
    if os.path.exists(LOG_FILE):
        logs = load_json(LOG_FILE)
    else:
        logs = {'replies': []}
    
    logs['replies'].append(reply)
    save_json(LOG_FILE, logs)


def process_inbox() -> int:
    """
    受信トレイを処理する
    Returns: 処理したメール数
    """
    inbox_data = load_json(INBOX_FILE)
    patterns_data = load_json(PATTERNS_FILE)
    
    processed_count = 0
    
    for email in inbox_data['inbox']:
        if email['processed']:
            continue
        
        print(f"\n{'='*50}")
        print(f"📧 新着メール検出!")
        print(f"   From: {email['from']}")
        print(f"   Subject: {email['subject']}")
        print(f"   受信時刻: {email['received_at']}")
        
        # 最適なパターンを検索（RAG）
        combined_text = f"{email['subject']} {email['body']}"
        best_pattern = find_best_pattern(combined_text, patterns_data['patterns'])
        
        print(f"\n🔍 RAG検索結果:")
        print(f"   マッチカテゴリ: {best_pattern['category']}")
        
        # 返信を生成
        reply = generate_reply(email, best_pattern)
        
        print(f"\n✉️ 返信案を生成:")
        print(f"   To: {reply['to']}")
        print(f"   Subject: {reply['subject']}")
        print(f"   ---")
        # 返信本文の最初の3行を表示
        body_preview = '\n'.join(reply['body'].split('\n')[:3])
        print(f"   {body_preview}")
        print(f"   ...")
        
        # ログに記録
        log_reply(reply)
        
        # 処理済みフラグを立てる
        email['processed'] = True
        processed_count += 1
        
        print(f"\n✅ ログに保存しました: {LOG_FILE}")
    
    # 受信トレイを更新
    save_json(INBOX_FILE, inbox_data)
    
    return processed_count


def main():
    """メインループ - 常駐して定期的に受信トレイをチェック"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║     📚 バリューブックス 自動返信ボット v1.0                  ║
║     n8n不要！Pythonだけで自動化を実現                        ║
╚══════════════════════════════════════════════════════════════╝
    """)
    print(f"⚙️  設定:")
    print(f"   チェック間隔: {CHECK_INTERVAL}秒")
    print(f"   受信トレイ: {INBOX_FILE}")
    print(f"   パターンDB: {PATTERNS_FILE}")
    print(f"   ログ出力: {LOG_FILE}")
    print(f"\n🚀 ボットを起動しました。Ctrl+C で停止できます。")
    print(f"{'='*60}")
    
    try:
        while True:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n⏰ [{current_time}] 受信トレイをチェック中...")
            
            processed = process_inbox()
            
            if processed > 0:
                print(f"\n📊 {processed}件のメールを処理しました")
            else:
                print(f"   → 未処理のメールはありません")
            
            print(f"\n💤 次のチェックまで{CHECK_INTERVAL}秒待機...")
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print(f"\n\n🛑 ボットを停止しました")
        print(f"   処理ログは {LOG_FILE} に保存されています")


if __name__ == "__main__":
    main()



