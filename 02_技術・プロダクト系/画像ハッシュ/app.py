import os
import json
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
from hasher import generate_hash, calculate_distance

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'static/processed_images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# 必要なフォルダを作成
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def load_database():
    """データベースを読み込む"""
    with open('database.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_similarity_percentage(distance):
    """
    複合距離スコアから類似度パーセンテージを計算
    distance: 0-100のスコア（低いほど類似）
    """
    if distance >= 100:
        return 0.0
    # 距離スコアを類似度に変換（距離が小さいほど類似度が高い）
    similarity = max(0, 100 - distance)
    return round(similarity, 1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if 'image' not in request.files:
        return jsonify({'error': '画像がアップロードされていません'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'ファイルが選択されていません'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': '許可されていないファイル形式です'}), 400

    # ファイルを保存
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # 前処理済み画像の保存先（検索用クエリ画像も前処理済みを保存）
        processed_filename = f"query_{filename}"
        processed_filepath = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)

        # アップロードされた画像のハッシュを生成（前処理済み画像も保存）
        query_hash = generate_hash(filepath, save_processed=True, processed_output_path=processed_filepath)

        if not query_hash:
            return jsonify({'error': '画像の処理に失敗しました'}), 500

        # データベースと照合
        db_data = load_database()
        results = []

        for db_item in db_data:
            distance = calculate_distance(query_hash, db_item['hash'])
            similarity = calculate_similarity_percentage(distance)

            # 前処理済み画像のパスを確認
            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], db_item['filename'])

            # 前処理済み画像が存在する場合はそれを使用、なければ元画像を使用
            if os.path.exists(processed_path):
                image_url = url_for('static', filename=f'processed_images/{db_item["filename"]}')
            else:
                image_url = url_for('static', filename=f'images_db/{db_item["filename"]}')

            results.append({
                'filename': db_item['filename'],
                'distance': distance,
                'similarity': similarity,
                'image_url': image_url
            })

        # 距離が近い順にソートして上位10件を取得
        results.sort(key=lambda x: x['distance'])
        top_results = results[:10]

        # アップロードファイルを削除（前処理済み画像は残す）
        os.remove(filepath)

        return jsonify({
            'success': True,
            'results': top_results,
            'query_image_url': url_for('static', filename=f'processed_images/{processed_filename}')
        })

    except Exception as e:
        # エラー時はアップロードファイルと前処理済みファイルを削除
        if os.path.exists(filepath):
            os.remove(filepath)
        if 'processed_filepath' in locals() and os.path.exists(processed_filepath):
            os.remove(processed_filepath)
        return jsonify({'error': f'検索中にエラーが発生しました: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
