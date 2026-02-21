import os
import json
import argparse
from hasher import generate_hash, calculate_distance

class BookFingerprint:
    def __init__(self, db_path='database.json', images_db_dir='images_db', query_dir='images_query', processed_dir='static/processed_images'):
        self.db_path = db_path
        self.images_db_dir = images_db_dir
        self.query_dir = query_dir
        self.processed_dir = processed_dir
        self.db_data = self._load_db()

        # 前処理済み画像用ディレクトリを作成
        os.makedirs(self.processed_dir, exist_ok=True)

    def _load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _save_db(self):
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.db_data, f, ensure_ascii=False, indent=4)

    def register(self):
        """
        images_db フォルダ内の画像をスキャンし、ハッシュ値をDBに保存する。
        同時に前処理済み画像も保存する。
        """
        print(f"--- 登録モード開始: {self.images_db_dir} ---")
        if not os.path.exists(self.images_db_dir):
            print(f"Error: {self.images_db_dir} フォルダが見つかりません。")
            return

        # 現在のDBを辞書形式にして更新しやすくする
        current_db = {item['filename']: item['hash'] for item in self.db_data}
        updated_count = 0

        for filename in os.listdir(self.images_db_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(self.images_db_dir, filename)
                print(f"Processing: {filename}...", end='\r')

                # 前処理済み画像の保存先パス
                processed_path = os.path.join(self.processed_dir, filename)

                # ハッシュ生成と同時に前処理済み画像を保存
                img_hash = generate_hash(file_path, save_processed=True, processed_output_path=processed_path)
                if img_hash:
                    current_db[filename] = img_hash
                    updated_count += 1

        # リスト形式に戻して保存
        self.db_data = [{"filename": k, "hash": v} for k, v in current_db.items()]
        self._save_db()
        print(f"\n完了: {updated_count} 件の画像を登録/更新しました。")
        print(f"前処理済み画像は {self.processed_dir} に保存されました。")

    def search(self, threshold=5):
        """
        images_query フォルダ内の画像をスキャンし、DBと照合する。
        """
        print(f"--- 検索モード開始: {self.query_dir} (閾値: {threshold}) ---")
        if not self.db_data:
            print("Error: データベースが空です。先に登録を実行してください。")
            return

        if not os.path.exists(self.query_dir):
            print(f"Error: {self.query_dir} フォルダが見つかりません。")
            return

        query_files = [f for f in os.listdir(self.query_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not query_files:
            print("検索用画像が見つかりません。")
            return

        for q_filename in query_files:
            q_path = os.path.join(self.query_dir, q_filename)
            q_hash = generate_hash(q_path)
            
            if not q_hash:
                continue

            results = []
            for db_item in self.db_data:
                distance = calculate_distance(q_hash, db_item['hash'])
                if distance <= threshold:
                    results.append({
                        "filename": db_item['filename'],
                        "distance": distance
                    })

            # 距離が近い順にソート
            results.sort(key=lambda x: x['distance'])

            print(f"\n[検索画像]: {q_filename}")
            if results:
                for res in results:
                    print(f"  [一致] 対象: {res['filename']} (距離: {res['distance']})")
            else:
                print("  一致する本は見つかりませんでした。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BookFingerprint - アナログ本 同定システム')
    parser.add_argument('mode', choices=['register', 'search'], help='実行モード (register: 登録, search: 検索)')
    parser.add_argument('--threshold', type=int, default=5, help='検索時のハミング距離閾値 (デフォルト: 5)')
    
    args = parser.parse_args()
    
    app = BookFingerprint()
    
    if args.mode == 'register':
        app.register()
    elif args.mode == 'search':
        app.search(threshold=args.threshold)
