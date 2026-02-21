import imagehash
from PIL import Image, ImageFilter, ImageEnhance
import json
import numpy as np
import cv2

def detect_book_object(img):
    """
    物体検出で本領域を抽出
    エッジベースの検出で最も大きい矩形領域を本として検出
    """
    # PIL画像をOpenCV形式に変換
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    original_height, original_width = img_cv.shape[:2]

    # グレースケール変換
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # 適応的二値化（照明の変化に強い）
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )

    # ノイズ除去
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

    # 輪郭検出
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return img

    # 面積が大きい順にソート
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # 最も大きい輪郭を取得（本の可能性が高い）
    for contour in contours[:3]:  # 上位3つを試す
        contour_area = cv2.contourArea(contour)
        image_area = original_width * original_height

        # 面積が画像全体の15%以上、95%以下の場合のみ処理
        if contour_area < image_area * 0.15 or contour_area > image_area * 0.95:
            continue

        # バウンディングボックスを取得
        x, y, w, h = cv2.boundingRect(contour)

        # アスペクト比をチェック（本は縦長または横長の矩形）
        aspect_ratio = float(w) / h if h > 0 else 0
        if aspect_ratio < 0.4 or aspect_ratio > 2.5:
            continue

        # 本領域を切り抜き
        margin = 10  # 少し余白を持たせる
        y1 = max(0, y - margin)
        y2 = min(original_height, y + h + margin)
        x1 = max(0, x - margin)
        x2 = min(original_width, x + w + margin)

        cropped = img_cv[y1:y2, x1:x2]

        # OpenCV形式からPIL画像に変換
        cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
        return Image.fromarray(cropped_rgb)

    # 本が検出できない場合は元の画像を返す
    return img

def detect_and_correct_perspective(img):
    """
    物体検出 + 輪郭検出と台形補正（パースペクティブ変換）
    """
    # まず本領域を検出して切り抜き
    img = detect_book_object(img)

    # PIL画像をOpenCV形式に変換
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    original_height, original_width = img_cv.shape[:2]

    # グレースケール変換
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # ガウシアンブラーでノイズ除去
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # エッジ検出
    edges = cv2.Canny(blurred, 50, 150)

    # 輪郭検出
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return img

    # 面積が最も大きい輪郭を取得
    largest_contour = max(contours, key=cv2.contourArea)

    # 輪郭の面積が画像全体の10%以上の場合のみ処理
    contour_area = cv2.contourArea(largest_contour)
    image_area = original_width * original_height

    if contour_area < image_area * 0.1:
        return img

    # 輪郭を近似して四角形を検出
    peri = cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, 0.02 * peri, True)

    # 4点の四角形が検出できた場合のみ台形補正
    if len(approx) == 4:
        # 四角形の4点を取得
        pts = approx.reshape(4, 2).astype(np.float32)

        # 点を左上、右上、右下、左下の順に並べ替え
        rect = order_points(pts)

        # 変換後の幅と高さを計算
        width = int(max(
            np.linalg.norm(rect[0] - rect[1]),
            np.linalg.norm(rect[2] - rect[3])
        ))
        height = int(max(
            np.linalg.norm(rect[0] - rect[3]),
            np.linalg.norm(rect[1] - rect[2])
        ))

        # 変換後の座標
        dst = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype=np.float32)

        # パースペクティブ変換行列を計算
        matrix = cv2.getPerspectiveTransform(rect, dst)

        # 台形補正を適用
        warped = cv2.warpPerspective(img_cv, matrix, (width, height))

        # OpenCV形式からPIL画像に変換
        warped_rgb = cv2.cvtColor(warped, cv2.COLOR_BGR2RGB)
        return Image.fromarray(warped_rgb)

    # 4点の四角形が検出できない場合は元の画像を返す
    return img

def order_points(pts):
    """
    4点を左上、右上、右下、左下の順に並べ替え
    """
    rect = np.zeros((4, 2), dtype=np.float32)

    # 合計が最小のものが左上、最大のものが右下
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # 差分が最小のものが右上、最大のものが左下
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def preprocess_image(img):
    """
    背景の影響を軽減するための前処理
    """
    # 画像をRGB変換（PNGなどのアルファチャンネル対応）
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # 台形補正（パースペクティブ変換）
    img = detect_and_correct_perspective(img)

    # コントラスト強調（本の表紙の特徴を際立たせる）
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)

    # シャープネス強調（エッジを明確に）
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.3)

    return img

def crop_center_region(img, crop_ratio=0.85):
    """
    画像の中央部分を切り抜く（背景の影響を減らす）
    crop_ratio: 切り抜く範囲（0.85 = 85%の領域を使用）
    """
    width, height = img.size

    # 中央から指定比率の領域を切り抜く
    new_width = int(width * crop_ratio)
    new_height = int(height * crop_ratio)

    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = left + new_width
    bottom = top + new_height

    return img.crop((left, top, right, bottom))

def generate_hash(image_path, save_processed=False, processed_output_path=None):
    """
    画像パスを受け取り、複数のハッシュ値を生成して返す。
    - phash: 形状・構造（グレースケール）
    - colorhash: 色情報
    - average_hash: 平均ハッシュ（補助）
    - dhash: 差分ハッシュ（背景に強い）

    Args:
        image_path: 入力画像のパス
        save_processed: 前処理済み画像を保存するかどうか
        processed_output_path: 前処理済み画像の保存先パス
    """
    try:
        img = Image.open(image_path)

        # 前処理：コントラスト・シャープネス強調
        img_processed = preprocess_image(img)

        # 中央領域を切り抜き（背景の影響を軽減）
        img_cropped = crop_center_region(img_processed, crop_ratio=0.85)

        # 前処理済み画像を保存（オプション）
        if save_processed and processed_output_path:
            img_cropped.save(processed_output_path, quality=95)

        # 形状ハッシュ（高精度）
        phash_val = imagehash.phash(img_cropped, hash_size=16)

        # 色ハッシュ（色の分布を捉える）
        colorhash_val = imagehash.colorhash(img_cropped, binbits=4)

        # 平均ハッシュ（補助的に使用）
        ahash_val = imagehash.average_hash(img_cropped, hash_size=16)

        # 差分ハッシュ（背景変化に強い）
        dhash_val = imagehash.dhash(img_cropped, hash_size=16)

        # 辞書形式で返す
        return {
            'phash': str(phash_val),
            'colorhash': str(colorhash_val),
            'ahash': str(ahash_val),
            'dhash': str(dhash_val)
        }
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def calculate_distance(hash1_dict, hash2_dict):
    """
    2つのハッシュ辞書間の総合距離を計算する。
    重み付け: phash=40%, dhash=30%, colorhash=20%, ahash=10%
    dhashは背景変化に強いため重要度を上げる
    """
    if not hash1_dict or not hash2_dict:
        return float('inf')

    try:
        # 各ハッシュの距離を計算
        phash_dist = imagehash.hex_to_hash(hash1_dict['phash']) - imagehash.hex_to_hash(hash2_dict['phash'])
        colorhash_dist = imagehash.hex_to_hash(hash1_dict['colorhash']) - imagehash.hex_to_hash(hash2_dict['colorhash'])
        ahash_dist = imagehash.hex_to_hash(hash1_dict['ahash']) - imagehash.hex_to_hash(hash2_dict['ahash'])
        dhash_dist = imagehash.hex_to_hash(hash1_dict['dhash']) - imagehash.hex_to_hash(hash2_dict['dhash'])

        # 正規化（各ハッシュの最大距離で割る）
        # phash: 256ビット, colorhash: 約64ビット, ahash: 256ビット, dhash: 256ビット
        phash_normalized = phash_dist / 256.0
        colorhash_normalized = colorhash_dist / 64.0
        ahash_normalized = ahash_dist / 256.0
        dhash_normalized = dhash_dist / 256.0

        # 重み付け総合スコア（0-100スケール）
        # dhashの重みを増やして背景の影響を軽減
        combined_score = (
            phash_normalized * 40 +
            dhash_normalized * 30 +
            colorhash_normalized * 20 +
            ahash_normalized * 10
        )

        return combined_score
    except Exception as e:
        print(f"Error calculating distance: {e}")
        return float('inf')
