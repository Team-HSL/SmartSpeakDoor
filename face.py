
# coding: utf-8

# # Face API 操作関数

#キーの取得
file = open('key.txt')
subscription_key = file.read()

def getFaceID(image_url,subscription_key = subscription_key, plflag = 0, image_file = []):
    # 画像のfaceIDを取得する
    import requests
    
    import matplotlib.pyplot as plt
    from PIL import Image
    from matplotlib import patches
    from io import BytesIO
    
    #Jupyter Notebookを使っている場合は以下のマジックコマンドを使用
   # get_ipython().magic('matplotlib inline')
    
    face_api_url_detect = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
    
    #---------------------------------------------------- 画像の取得 ---------------------------------------------------------
    #"""
    #----1. webから取得する場合 ----#
    #画像のあるURLを指定
    data_url = {'url': image_url}
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    #"""
    
    #---- Localから取得する場合 ----#  
    # 画像へのパスをimage_fileに代入
    if image_file:
        data_url = open(image_file, "rb").read()

        headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                      'Content-Type': 'application/octet-stream'}
  
    #------------------------------------------------------- 画像から取得したい情報の指定 -----------------------------------
    # 'returnFaceId': 入力した顔画像に付与されるIDを返すかどうか
    # 'returnFaceLandmarks' : 目や口などの特徴となる部分の座標を返すかどうか
    # 'returnFaceAttributes' :　認識した顔からわかる属性を返す
    #   指定できるパラメータは以下で、コンマで分けて複数指定可能
    #       age, gender, headPose, smile, facialHair, 
    #       glasses, emotion, hair, makeup, occlusion, 
    #       accessories, blur, exposure and noise
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
        'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }
    
    #------------------------------------------------------- httpにリクエストを送る(データを取ってくる) -----------------------------------
    #"""
    #----1. web画像の場合 ----#
    response_url = requests.post(face_api_url_detect, params=params, headers=headers, json=data_url)
    #"""
    
    faces = response_url.json()
    
    faceIds = []
    for face in faces:
        faceIds.append(face["faceId"])
    
    #------------------------------------------------------- 結果の表示 -----------------------------------
    #今回は入力画像の顔を検知し，性別と年齢の情報を表示させる
    if plflag == 1:
        #"""
        #----1. web画像の場合 ----#
        image_url = Image.open(BytesIO(requests.get(image_url).content))
        #"""

        plt.figure(figsize=(8, 8))
        ax = plt.imshow(image_url, alpha=0.6)
        for face in faces:
            fr = face["faceRectangle"]
            fa = face["faceAttributes"]
            ID = face["faceId"]
            origin = (fr["left"], fr["top"])
            p = patches.Rectangle(
                origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
            ax.axes.add_patch(p)
            plt.text(origin[0], origin[1], "%s, %d"%(fa["gender"].capitalize(), fa["age"]),
                     fontsize=20, weight="bold", va="bottom")
#            plt.text(origin[0], origin[1], "%s"%ID, fontsize=10, weight="bold", va="bottom")
        _ = plt.axis("off")
        
    return faceIds


def createFacelist(Facelistname, subscription_key = subscription_key, image_file=[]):
    # facelist作成
    import requests
    face_api_url_facelist  = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/facelists/'  + Facelistname

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    #---- Localから取得する場合 ----#  
    # 画像へのパスをimage_fileに代入
    if image_file:
        image_data = open(image_file, "rb").read()

        headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                      'Content-Type': 'application/octet-stream'}
    
    data_facelist = {"name": Facelistname}
    response_tamorist = requests.put(face_api_url_facelist, params={}, headers=headers, json=data_facelist)
    json_tamorist = response_tamorist.json()
    
    return json_tamorist


def getFacelistIDs(subscription_key = subscription_key, image_file=[]):
    # facelistID取得
    import requests
    face_api_url_facelistget  = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/facelists'
    
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    #---- Localから取得する場合 ----#  
    # 画像へのパスをimage_fileに代入
    if image_file:
        image_data = open(image_file, "rb").read()

        headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                      'Content-Type': 'application/octet-stream'}
    
    response_tamoristID = requests.get(face_api_url_facelistget, params={}, headers=headers)
    json_tamoristID = response_tamoristID.json()
    
    return json_tamoristID


def deleteFacelist(Facelistname, subscription_key = subscription_key, image_file=[]):
    # ID から facelist を消去する
    import requests
    face_api_url_facelistDelete  = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/facelists/' + Facelistname
    
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    #---- Localから取得する場合 ----#  
    # 画像へのパスをimage_fileに代入
    if image_file:
        image_data = open(image_file, "rb").read()
        headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                      'Content-Type': 'application/octet-stream'}
        
    response_tamotamo = requests.delete(face_api_url_facelistDelete, params={}, headers=headers)
    json_tamotamo = response_tamotamo.json()
    return json_tamotamo
    

def addFace2Facelist(image_url, faceListname, faceListID, subscription_key = subscription_key, image_file=[]):
    # facelistに顔を追加
    import requests
    face_api_url_facelist  = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/facelists/' + faceListname + '/persistedFaces'
    
    #---------------------------------------------------- 画像の取得 ---------------------------------------------------------
    #"""
    #----1. webから取得する場合 ----#
    #画像のあるURLを指定
    data_url = {'url': image_url}
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    #"""
    
    #---- Localから取得する場合 ----#  
    # 画像へのパスをimage_fileに代入
    if image_file:
        data_url = open(image_file, "rb").read()
        headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                      'Content-Type': 'application/octet-stream'}
    
    params = {'faceListId': faceListID}
    response_tamory = requests.post(face_api_url_facelist, params=params, headers=headers, json=data_url)
    json_tamory = response_tamory.json()

    return json_tamory


def getFaceSimilarity(targetFaceID, faceListID, subscription_key = subscription_key, image_file=[]):
    # 類似度の取得
    import requests
    face_api_url_findsimilars = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/findsimilars'

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    #---- Localから取得する場合 ----#  
    # 画像へのパスをimage_fileに代入
    if image_file:
        image_data = open(image_file, "rb").read()

        headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                      'Content-Type': 'application/octet-stream'}
        
    data_judge = {
        "faceId": targetFaceID,
        "faceListId": faceListID,
        "maxNumOfCandidatesReturned": 10,
        "mode": "matchPerson"
    }

    response_tamosimi = requests.post(face_api_url_findsimilars, params={}, headers=headers, json=data_judge)
    # facesに画像解析結果のjsonファイルを格納
    tamori_similarity = response_tamosimi.json()

    return tamori_similarity


def meanConf(similarity_list_dict):
    # 類似度の平均を計算する
    S = 0
    N = len(similarity_list_dict)
    for i in range(N):
        S += similarity_list_dict[i]["confidence"]
        
    return S / N


def test(faceListname):
    # initialization
    image_sanma1 = "http://haaasoku.com/wp-content/uploads/2014/04/" +                                     "%E6%98%8E%E7%9F%B3%E5%AE%B6%E3%81%95%E3%82%93%E3%81%BE%EF%BC%921.jpg"
    image_sanma2 = "https://grapee.jp/wp-content/uploads/37312_main.jpg"
    image_sanma3 = "http://image.news.livedoor.com/newsimage/stf/d/6/d6885_929_spnldpc-20180904-0080-003-p-0.jpg"
    
    image_url =  'https://www.sankei.com/images/news/170126/ent1701260002-p5.jpg'
    
    # ID 取得
    sanma1ID = getFaceID(image_sanma1,plflag=1)
    sanma2ID = getFaceID(image_sanma2,plflag=1)
    sanma3ID = getFaceID(image_sanma3,plflag=1)
    
    image_urlIDs = getFaceID(image_url,plflag=1)
    
        # Facelist 新規作成
#    json_facelistcreation = createFacelist(faceListname)
#    print(json_facelistcreation)
    
    # Facelist ID 取得
    json_SanmaFLID = getFacelistIDs()
    for i in range(len(json_SanmaFLID)):
        if json_SanmaFLID[i]['name'] == faceListname:
            faceListID = json_SanmaFLID[i]['faceListId'] 

    # Facelist に 顔を入れる
    json_sanmary1 = addFace2Facelist(image_sanma1, faceListname, faceListID)
    json_sanmary2 = addFace2Facelist(image_sanma2, faceListname, faceListID)
    json_sanmary3 = addFace2Facelist(image_sanma3, faceListname, faceListID)
    
    # それぞれの顔の類似度を取得
    sanma_simsdict = {}
    for kaoID in image_urlIDs:
        sim_list_dict = getFaceSimilarity(kaoID, faceListID)
        sanma_simsdict[kaoID] = sim_list_dict
    
    # 類似度の高い顔のIDを抽出
    simHighest = 0.8
    otherID = []
    Sanma_ID = ''
    for kao, sim_list_dict in sanma_simsdict.items():
        if sim_list_dict:
            simtemp = meanConf(sim_list_dict)
        else: simtemp = 0
        if simtemp > simHighest:
            Sanma_ID = kao
            simHighest = simtemp
        else: otherID.append(kao)
    
    # Facelist 削除
#    deleteFacelist(faceListname)

    
    return [Sanma_ID, otherID]
    

if __name__ == "__main__":    
    faceListname = "akashiya_sanma"
    
    createFacelist(faceListname)
    print(test(faceListname))
    
#    deleteFacelist(faceListname)