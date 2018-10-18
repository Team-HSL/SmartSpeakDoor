import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("tatsuya", frame)
    cv2.imwrite('picture/muraki.jpg', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;
cap.release()
cv2.destroyAllWindows()


'''
Microsoft AzureのFace APIのサンプルコードです．
web上の画像とローカル画像のどちらにも対応できます．
ただし，webとローカルの切り替えを行う場合に変更するポイントが3つあるので注意してください．

画像はJPEG, PNG, GIF, BMPに対応

参照：https://docs.microsoft.com/ja-jp/azure/cognitive-services/face/quickstarts/python
'''


#------------------------------------------------------　ライブラリのインポート -----------------------------------
import requests
#
#
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO

#Jupyter Notebookを使っている場合は以下のマジックコマンドを使用
#%matplotlib inline

#------------------------------------------------------- API情報を入力 -----------------------------------
file = open('key.txt')
key = file.read()



# キーを入力
subscription_key = key
assert subscription_key

#与えられたキーのエンドポイントを入力する．　
#7日間無料試用アカウントの場合は変更の必要なし．
#アカウントによっては「westcentralus」の部分を変更しなければならない
face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'



#------------------------------------------------------- 画像データの指定 -----------------------------------
"""
#----1. webから取得する場合 ----#
#画像のあるURLを指定
image_url = 'https://how-old.net/Images/faces2/main007.jpg'
data = {'url': image_url}
headers = {'Ocp-Apim-Subscription-Key': subscription_key}
"""

#"""
#----2. Localから取得する場合 ----#
# 画像へのパスをimage_fileに代入

#パスは個人で変更してください（下の二箇所）

image_file ="./picture/muraki.jpg"
image_data = open(image_file, "rb").read()
from PIL import Image
image_data2 = Image.open("./picture/muraki.jpg")
image_data2.show()

headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
              'Content-Type': 'application/octet-stream'}
#"""

#------------------------------------------------------- 画像から取得したい情報の指定 -----------------------------------
# 'returnFaceId': 入力した顔画像に付与されるIDを返すかどうか
# 'returnFaceLandmarks' : 目や口などの特徴となる部分の座標を返すかどうか
# 'returnFaceAttributes' :　認識した顔からわかる属性を返す
#   指定できるパラメータは以下で、コンマで分けて複数指定可能
#       age, gender, headPose, smile, facialHair,
#       glasses, emotion, hair, makeup, occlusion,
#       accessories, blur, exposure and noise
params = {
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
    'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
}


#------------------------------------------------------- httpにリクエストを送る(データを取ってくる) -----------------------------------
"""
#----1. web画像の場合 ----#
response = requests.post(face_api_url, params=params, headers=headers, json=data)

"""

#"""
#----2. Local画像の場合 ----#
response = requests.post(
    face_api_url, headers=headers, params=params, data=image_data)
#"""

# facesに画像解析結果のjsonファイルを格納
faces = response.json()
print(faces)

#------------------------------------------------------- 結果の表示 -----------------------------------
#今回は入力画像の顔を検知し，性別と年齢の情報を表示させる
"""
----1. web画像の場合 ----#
image = Image.open(BytesIO(requests.get(image_url).content))
"""

#"""
#----2. Local画像の場合 ----#
image = Image.open(BytesIO(image_data))
#"""

plt.figure(figsize=(8, 8))
ax = plt.imshow(image, alpha=0.6)
for face in faces:
    fr = face["faceRectangle"]
    fa = face["faceAttributes"]
    origin = (fr["left"], fr["top"])
    p = patches.Rectangle(
        origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
    ax.axes.add_patch(p)
    plt.text(origin[0], origin[1], "%s, %d"%(fa["gender"].capitalize(), fa["age"]),
             fontsize=20, weight="bold", va="bottom")
_ = plt.axis("off")