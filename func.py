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
from cognitive_face import util


# Key情報の入力
key_file = open('key.txt')
SUBSCRIPTION_KEY = key_file.read()
key_file.close()

BASE_URL = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)


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

#情報を返す部分
def api(id):

    from train_api import train_api
    from calender_api import calender_api
    from weather_api import weather_api

    if id == 1:
        name = '後藤さん'
        via = '25717:25635' # from出町柳to河原町
        lat = '35.01' # 河原町緯度
        lon = '135.76' # 河原町経度
        calenderID = '8e5etm3bvc22pgjj60795lel2s@group.calendar.google.com' # Goto ID

    elif id == 2:
        name = '村木くん'
        via = '25717:26238' # from出町柳to淀屋橋
        lat = '34.69' # 淀屋橋緯度
        lon = '135.50' # 淀屋橋経度
        calenderID = 'cad895h1svqfv2bdls4mppsbag@group.calendar.google.com'
    else:
        str = 'あなたは登録されていません。'

    tdatetime, hour, minute, second = train_api(via) # tdatetime is date. others are str.
    weather = weather_api(lat, lon)
    eventlist, startlist = calender_api(calenderID) # list returned

    train = hour + '時' + minute + '分' + 'に発車します。'
    weather = '今日は' + weather + 'です。'
    schedule = '予定は' + eventlist[0] + 'が近いです。'

    # these lines will be deleted.
    print(name)
    print(train)
    print(weather)
    print(schedule)

    return name, train, weather, schedule



#喋る部分
def talk(talklist):

    import sys
    import os
    import subprocess
    from time import sleep
    sys.path.append('./api_code')
    def jtalk(t, num):
        open_jtalk = ['open_jtalk']
        mech = ['-x', '/usr/local/Cellar/open-jtalk/1.10_1/dic']
        htsvoice = ['-m', '/usr/local/Cellar/open-jtalk/1.10_1/voice/mei/mei_normal.htsvoice']
        speed = ['-r', '0.8']
        outwav = ['-ow', 'ja_sound/ja_{}.wav'.format(num)]
        cmd = open_jtalk + mech + htsvoice + speed + outwav
        c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        c.stdin.write(t)
        c.stdin.close()
        c.wait()
        # 音声を再生する場合
    
        aplay = ['afplay', 'ja_sound/ja_{}.wav'.format(num)]
        wr = subprocess.Popen(aplay)

    os.system('rm -rf ja_sound')
    os.system('mkdir ja_sound')
    for i, x in enumerate(talklist):
        jtalk(x.encode('utf-8'), i)
        sleep(3)



#image_byteに画像のバイト列を代入して，その画像中の人物リストを得る
def get_person_kind(image_byte):
    PERSON_GROUP_ID = 'hsluser'
    # 既存のPeron Groupがあるかどうかで挙動を変える．
    # おそらくAzureでは24時間Person Groupの情報が保存されるようなので，24時間たったかどうかで分岐させるのが良いかも
    # この状態では新たな人を登録したいとき，1度だけ実行されるプログラムを書くか，
    # 一度Person groupをCF.person_group.delete(PERSON_GROUP_ID)で削除してからtryの中身をを変更する必要がある．

    try:
        CF.person_group.create(PERSON_GROUP_ID, 'Hsluser')

        #人の画像を登録する．
        create_person_group(PERSON_GROUP_ID, name='YUki Goto', folder_name='yuki', user_data='beautiful')
        create_person_group(PERSON_GROUP_ID, name='Tatsuya Muraki', folder_name='tatsuya', user_data='genius')

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

    # 通常のFace APIをたたく
    response = detect_(image_byte, face_id=True, landmarks=True, attributes='age,gender')
    face_ids = [d['faceId'] for d in response]
    print(face_ids)

    identified_faces = CF.face.identify(face_ids, PERSON_GROUP_ID)
    print(identified_faces)


    name_id_dict = {}
    for person in CF.person.lists(PERSON_GROUP_ID):
        name = person['name']
        Id = person['personId']
        detail = person['userData']
        name_id_dict[Id] = {'name': name, 'userData' : detail}

    person_kind = []
    face_dict = {}
    for face in identified_faces:
        if face['candidates'] == []:
            personID = ''
            name=''
            faceID = face['faceId']
            face_dict[faceID] = {}
            print('anyone')

        else:
            personID = face['candidates'][0]['personId']
            faceID = face['faceId']
            name = name_id_dict[personID]['name']
            detail = name_id_dict[personID]['userData']
            face_dict[faceID] = {'name': name, 'userData':detail}
        print(name)

        if name == 'YUki Goto':
            person_kind.append(1)
        if name == 'Tatsuya Muraki':
            person_kind.append(2)
        
    print('person_kind:',person_kind)        
    return person_kind     

#実行したい部分
def main(image_byte):
    person_kind = get_person_kind(image_byte)
    if person_kind:
        for id in person_kind:
            import sys
            sys.path.append('./api_code')
            name, train, weather, schedule = api(id)
            talklist = [name, train,schedule]

            sys.path.append('./api_code')
            # talk(talklist)
    else:
        import sys
        talklist = ['あなたはだれ']
        sys.path.append('./api_code')
        # talk(talklist)

if __name__ == '__main__':
    test_image = 'test_picture/test1.jpg'
    image_byte = open(test_image,'rb').read()
    main(image_byte)