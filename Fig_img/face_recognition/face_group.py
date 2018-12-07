#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 15:54:22 2018

@author: abetakuto
"""

'''
cognitive_faceというモジュールをダウンロードする必要あり．
実行する際は，Face APIのkeyとBase_URLを各自変更してください．
参考：https://clemenssiebler.com/face-recognition-with-azure-cognitive-services-face-api/
'''


import requests
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO
import glob
import cognitive_face as CF


# Key情報の入力
key_file = open('../key/key_face.txt')
SUBSCRIPTION_KEY = key_file.read()
key_file.close()

BASE_URL = 'https://eastasia.api.cognitive.microsoft.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)


"""
The Face API uses the concept of person groups and persons:
・A person group contains zero or more persons and is referred to by a person_group_id
・A person is identified by a person_id and has a name and some custom user data
・A person has zero or more face images associated to it
"""


def create_person_group(PERSON_GROUP_ID, name, folder_name, user_data=''):
    """
    入力
        PERSON_GROUP_ID : Azureのどのグループに保存したいかを指定
        name : str型，登録したい人の名前
        folder_name : str型，登録したい人の画像を格納したフォルダー名(このpythonファイルと同じフォルダー内にあるもの)
        user_data : str型，登録した人の追加情報を一緒に登録することができる
    出力
        result
        一応出力させているだけであるが，Person Groupに最後の人を登録した時のresultを
        見ると，Person Groupの情報をlist形式でみることができる．
    """
    response = CF.person.create(PERSON_GROUP_ID, name, user_data)
    person_id = response['personId']
    image_lst = glob.glob('./{}/*'.format(folder_name))
    for image in image_lst:
        CF.person.add_face(image, PERSON_GROUP_ID, person_id)
    result = CF.person.lists(PERSON_GROUP_ID).copy()
    return result




PERSON_GROUP_ID = 'audrey'
# 既存のPeron Groupがあるかどうかで挙動を変える．
# おそらくAzureでは24時間Person Groupの情報が保存されるようなので，24時間たったかどうかで分岐させるのが良いかも
# この状態では新たな人を登録したいとき，1度だけ実行されるプログラムを書くか，
# 一度Person groupをperson_group.delete(PERSON_GROUP_ID)で削除してからtryの中身をを変更する必要がある．
try:
    CF.person_group.create(PERSON_GROUP_ID, 'Audrey')
    
    #人の画像を登録する．
    create_person_group(PERSON_GROUP_ID, name='Kasuga Toshiaki', folder_name='kasuga', user_data='Boke')
    create_person_group(PERSON_GROUP_ID, name='Wakabayashi Masayasu', folder_name='wakabayashi', user_data='Tsukkomi')
     
    # 画像を学習させる
    CF.person_group.train(PERSON_GROUP_ID)
    
    
    # As training is running asynchronously and thus not might happen immediately,
    # we need to check the status to make sure it has completed:
    response = CF.person_group.get_status(PERSON_GROUP_ID)
    status = response['status']
    print(status)

    
except:
    pass


# --------------------- テスト画像で学習ができているかを確認  --------------------------------
# 将来的にはconfidenceの情報を利用してみるのもいいかも

test_image = 'test_picture/test2.jpg'
# 通常のFace APIをたたく
response = CF.face.detect(test_image, face_id=True, landmarks=True, attributes='age,gender')
face_ids = [d['faceId'] for d in response]
#print(face_ids)

identified_faces = CF.face.identify(face_ids, PERSON_GROUP_ID)
#print(identified_faces)


name_id_dict = {}
for person in CF.person.lists(PERSON_GROUP_ID):
    name = person['name']
    Id = person['personId']
    detail = person['userData']
    name_id_dict[Id] = {'name': name, 'userData' : detail}


face_dict = {}
for face in identified_faces:
    if face['candidates'] == []:
        personID = ''
        faceID = face['faceId']
        face_dict[faceID] = {}

    else:
        personID = face['candidates'][0]['personId']
        faceID = face['faceId']
        name = name_id_dict[personID]['name']
        detail = name_id_dict[personID]['userData']
        face_dict[faceID] = {'name': name, 'userData':detail}

# ------------------------  可視化 ----------------
image_data = open(test_image, "rb").read()


image = Image.open(BytesIO(image_data))



plt.figure(figsize=(8, 8))
ax = plt.imshow(image, alpha=0.6)
for face in response:
    fr = face["faceRectangle"]
    fa = face["faceAttributes"]
    iD = face['faceId']
    if face_dict[iD] == {}:
        pass
    else:
        name = face_dict[iD]['name']
        detail = face_dict[iD]['userData']
        origin = (fr["left"], fr["top"])
        p = patches.Rectangle(
            origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
        ax.axes.add_patch(p)
        plt.text(origin[0], origin[1], "%s \n %s"%(name, detail),
                 fontsize=15, weight="bold", va="bottom")

_ = plt.axis("off")

