# 検出文字とBBox表示

from google.cloud import vision
from google.oauth2 import service_account
from PIL import Image, ImageDraw, ImageFont
import io

# APIキーのパス
key_path =r"C:\Users\TszHo\Desktop\book\arctic-plasma-405510-9e42a0a90b21.json"
# 画像上に文字描画するためのフォント
font_path = "C:\\Windows\\Fonts\\meiryo.ttc"  # Windowsの場合のMeiryoフォントのパス

# 初期化
credentials = service_account.Credentials.from_service_account_file(key_path)
client = vision.ImageAnnotatorClient(credentials=credentials)

# 画像のパス
image_path = '2.jpg'

# 画像の読み込み
with open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# テキスト検出の実行, text_annotation情報の取得
response = client.text_detection(image=image)
texts = response.text_annotations

# PILで画像を読み込む
pil_image = Image.open(io.BytesIO(content))
draw = ImageDraw.Draw(pil_image)
font = ImageFont.truetype(font_path, 70)  # 日本語フォントのパスを指定, 70:文字サイズ

# 最初のアノテーションは画像全体のテキストを含む。2番目以降のアノテーションで回す。
for text in texts[1:]:
    # BBoxの座標を取得
    vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
    
    # BBoxを画像に描画
    draw.polygon(vertices, outline='blue')
    
    # テキストを画像に描画 (座標は適当に調整)
    text_position = (vertices[0][0] - 50, vertices[0][1] - 70)
    draw.text(text_position, text.description, font=font, fill="blue")
    
    # 認識結果を実行結果に表示
    print(f"Text: {text.description}")
    print(f"Bounding Box: ({vertices[0][0]}, {vertices[0][1]}), ({vertices[1][0]}, {vertices[1][1]}), ({vertices[2][0]}, {vertices[2][1]}), ({vertices[3][0]}, {vertices[3][1]})")
    print()
    
# 画像を表示
pil_image.show()
