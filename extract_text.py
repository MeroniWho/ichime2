# 文字検出関数
from google.cloud import vision
from google.oauth2 import service_account
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import io

def extract_text_from_image(image_data, key_path=r"C:\Users\TszHo\Desktop\book\arctic-plasma-405510-9e42a0a90b21.json"):

    """
    画像からテキスト抽出
    input1 image_data: 入力画像データ
    input2 key_path: Google API キーのパス
    return 検索テキスト
    """

    #cho_center = (5000, 5000) # "著"BBox中心座標初期化
    # 検索ワード初期化
    search_text = ""
    #search_text=[]

    # 初期化
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    image_data = cv2.imread(image_data)
    # ノイズ除去
    image_data = cv2.GaussianBlur(image_data, (9, 9), 0)
    # コントラスト調整
    image_data = cv2.convertScaleAbs(image_data, alpha=1.5, beta=50)

    # OpenCVの画像をPIL形式に変換
    pil_image = Image.fromarray(cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB))

    # 画像をバイト形式に変換
    byte_io = io.BytesIO()
    pil_image.save(byte_io, format="JPEG")
    content = byte_io.getvalue()
    image = vision.Image(content=content)

    # テキスト検出
    response = client.document_text_detection(image=image)

    # BBox短辺長とテキスト検出の信頼度を保持するための配列
    short_sides_and_confidences = []

    # responseの中から信頼度, BBox, text取得
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    
                    confidence = word.confidence  # 信頼度スコア
                    bounding_box = [(vertex.x, vertex.y) for vertex in word.bounding_box.vertices] # BBox座標
                    word_text = ''.join([symbol.text for symbol in word.symbols]) # テキスト

                    if confidence >= 0.8:  # 信頼度が0.8以上のものに対して処理
                        # BBoxの短辺長の計算
                        side1 = ((bounding_box[0][0] - bounding_box[1][0])**2 + (bounding_box[0][1] - bounding_box[1][1])**2) ** 0.5
                        side2 = ((bounding_box[1][0] - bounding_box[2][0])**2 + (bounding_box[1][1] - bounding_box[2][1])**2) ** 0.5
                        short_side = min(side1, side2)
                        short_sides_and_confidences.append((short_side, confidence, word_text, bounding_box))
                        
                        #if word_text == '著':
                        #    cho_bounding_box = bounding_box
                        #    cho_center = ((cho_bounding_box[0][0] + cho_bounding_box[2][0]) / 2, (cho_bounding_box[0][1] + cho_bounding_box[2][1]) / 2)
                        #    cho_short_side = short_side

    if short_sides_and_confidences:
        # 信頼度が0.8以上の短辺の中で最も長いものを特定
        max_short_side = max(short_sides_and_confidences, key=lambda x: x[0])[0]
    else:
        max_short_side = None

    for short_side, confidence, word_text, bounding_box in short_sides_and_confidences:
        
        # BBox中心座標と"著"のBBox中心の距離
        #box_center = ((bounding_box[0][0] + bounding_box[2][0]) / 2, (bounding_box[0][1] + bounding_box[2][1]) / 2)
        #distance = ((cho_center[0] - box_center[0]) ** 2 + (cho_center[1] - box_center[1]) ** 2) ** 0.5

        # 検出文字のBBox短辺が最大BBox短辺より15pxcel差以内ならその情報を検索ワードに追加
        #if (distance < 100 and abs(short_side - cho_short_side) <= 30 and word_text != "著") or abs(max_short_side - short_side) <= 15:
        if max_short_side - short_side <= 15:
            search_text += word_text + "　"
            #search_text.append(word_text)
    #著の両隣によくある[]を取り除く用     
    #search_text = search_text.replace("[", "").replace("]", "")

    return search_text
    