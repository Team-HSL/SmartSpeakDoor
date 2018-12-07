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
from io import BytesIO
import glob
import cognitive_face as CF
from cognitive_face import util
# import winsound
import subprocess
from time import sleep
import os
import sys
import pprint

sys.path.append('./api_code')

from api_code.api import api
import pandas as pd

# Key情報の入力
key_file = open('key.txt')
SUBSCRIPTION_KEY = key_file.read()
key_file.close()

BASE_URL = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)


PERSON_GROUP_ID = 'hsluser2'


"""
The Face API uses the concept of person groups and persons:
・A person group contains zero or more persons and is referred to by a person_group_id
・A person is identified by a person_id and has a name and some custom user data
・A person has zero or more face images associated to it
"""


#imageにバイト列を入れると，
def detect_(image, face_id=True, landmarks=False, attributes=''):
    """Detect human faces in an image and returns face locations, and
    optionally with `face_id`s, landmarks, and attributes.
    Args:
        image: jpeg_byte code
        attributes: [Optional] Analyze and return the one or more specified
            face attributes in the comma-separated string like
            "age,gender". Supported face attributes include age, gender,
            headPose, smile, facialHair, glasses, emotion, makeup, accessories,
            occlusion, blur, exposure, noise. Note that each face attribute
            analysis has additional computational and time cost.
    Returns:
        An array of face entries ranked by face rectangle size in descending
        order. An empty response indicates no faces detected. A face entry may
        contain the corresponding values depending on input parameters.
    """
    url = 'detect'
    headers = {'Content-Type': 'application/octet-stream'}
    json = None
    data = image
    params = {
        'returnFaceId': face_id and 'true' or 'false',
        'returnFaceLandmarks': landmarks and 'true' or 'false',
        'returnFaceAttributes': attributes,
    }

    return util.request(
        'POST', url, headers=headers, params=params, json=json, data=data)



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

def jtalk(t, num):
        open_jtalk = ['open_jtalk']
        DICTIONARY_PATH = ['-x', 'C:/open_jtalk/bin/dic']
        VOICE_MODEL     = ['-m', 'C:/open_jtalk/bin/mei/mei_happy.htsvoice']
        SPEED = ['-r', '0.8']
        OUT_WAV = ['-ow', 'ja_sound/ja_{}.wav'.format(num)]
        cmd = open_jtalk + DICTIONARY_PATH + VOICE_MODEL + SPEED + OUT_WAV
        c = subprocess.Popen(cmd,stdin=subprocess.PIPE)

        # convert text encoding from utf-8 to shitf-jis
        c.stdin.write(t)
        c.stdin.close()
        c.wait()
        # play wav audio file with winsound module
        winsound.PlaySound(OUT_WAV[1], winsound.SND_FILENAME)

#喋る部分
def talk(talklist):
    # sys.path.append('./api_code')
    os.system('rm -rf ja_sound')
    os.system('mkdir ja_sound')
    talk_str = talklist[0] + "、" +talklist[1] + talklist[2] + talklist[3]
    jtalk(talk_str.encode('shift-jis'), 0)
    sleep(3)


def regist_name(csv_file_name):
# csvファイルからname_id_listを生成する．
# --------------------- 個人の顔画像データを登録 ----------------
#
    registered_names = set()
    for d in CF.person.lists(PERSON_GROUP_ID):
        registered_names.add(d["name"])
    
    print(registered_names)

    # try:
    #     CF.person_group.create(PERSON_GROUP_ID, 'Hsluser')
    # except:
    #     pass

    # ユーザーごとに画像登録を行う．
    # 名前でループ


    # df = pd.read_csv("SmartSpeakDoorList.csv")
    df = pd.read_csv(csv_file_name)
    print(df)
    name_list = df.name.values

    for name in name_list:
        if name not in registered_names:
            # nameの人が未登録の場合のみ，登録処理を行う．
            # 登録済みの場合はエラーが生じ，例外処理が行われる．
            try:
                #人の画像を登録する．
                create_person_group(PERSON_GROUP_ID, name=name, folder_name= './{}'.format(name))
            except:
                pass

        try:
            # 画像を学習させる
            CF.person_group.train(PERSON_GROUP_ID)

            # As training is running asynchronously and thus not might happen immediately,
            # we need to check the status to make sure it has completed:
            response = CF.person_group.get_status(PERSON_GROUP_ID)
            status = response['status']
            print(status)

        except:
            pass

    # Azureに事前に登録しておいた人物リストを取得する．
    name_id_dict = {}
    pprint.pprint(CF.person.lists(PERSON_GROUP_ID))

    for person in CF.person.lists(PERSON_GROUP_ID):
        name = person['name']
        Id = person['personId']
        detail = person['userData']
        name_id_dict[Id] = {'name': name, 'userData' : detail}
    # pprint.pprint(name_id_dict)

    return name_id_dict

#image_byteに画像のバイト列を代入して，その画像中の人物リストを得る
def get_person_kind(image_byte, name_id_dict):
    
    # 既存のPeron Groupがあるかどうかで挙動を変える．
    # おそらくAzureでは24時間Person Groupの情報が保存されるようなので，24時間たったかどうかで分岐させるのが良いかも
    # この状態では新たな人を登録したいとき，1度だけ実行されるプログラムを書くか，
    # 一度Person groupをCF.person_group.delete(PERSON_GROUP_ID)で削除してからtryの中身をを変更する必要がある．

    # --------------------- テスト画像で学習ができているかを確認  --------------------------------
    # 将来的にはconfidenceの情報を利用してみるのもいいかも

    # 通常のFace APIをたたく
    response = detect_(image_byte, face_id=True, landmarks=True, attributes='age,gender')
    face_ids = [d['faceId'] for d in response]
    print(len(face_ids))
    person_kind = []
    
    if face_ids:
        identified_faces = CF.face.identify(face_ids, PERSON_GROUP_ID)
        #print(identified_faces)

        # カメラ画像に映った人物を特定する．
        face_dict = {}
        for face in identified_faces:
            if face['candidates'] == []:
                personID = ''
                name=''
                faceID = face['faceId']
                face_dict[faceID] = {}
                print('誰でもない')
                return person_kind.append(3)

            else:
                personID = face['candidates'][0]['personId']
                faceID = face['faceId']
                name = name_id_dict[personID]['name']
                # detail = name_id_dict[personID]['userData']
                # face_dict[faceID] = {'name': name, 'userData':detail}
            # print(name)

        df = pd.read_csv("SmartSpeakDoorList.csv")
        df_query = df[df["name"]==name]
        
        return df_query.loc[0,["name", "city", "departure", "destination"]].to_dict()
    else:
        return None

#実行したい部分
def main():
    test_image = 'test_picture/tatsu_test.jpg'
    image_byte = open(test_image,'rb').read()
    name_id_dict = regist_name("SmartSpeakDoorList.csv")
    person_kind = get_person_kind(image_byte, name_id_dict=name_id_dict)

    if len(person_kind)>0:
        import sys
        sys.path.append('./api_code')
        name, train, weather, schedule = api(person_kind)
        talklist = [name, train, weather, schedule]

        talk(talklist)
    else:
        import sys
        talklist = ['あなたはだれ']
        sys.path.append('./api_code')
        talk(talklist)

if __name__ == '__main__':
    main()