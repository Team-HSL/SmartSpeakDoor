
import requests
import json
import datetime

def train_api(via):

    # APIキーの指定
    apikey = "test_G2zn3qudefX"

    # 出発地と目的地の並列化
    # via = '25717:25635' #これは'出町柳:河原町'

    # 経路探索するためのURL
    api = "http://api.ekispert.jp/v1/json/search/course/extreme?key={key}&viaList={via}&answerCount=1"

    # 実際にAPIにリクエストを送信して結果を取得する
    url = api.format(key=apikey, via=via)
    r = requests.get(url)

    # 結果はJSON形式なのでデコードする
    data = json.loads(r.text)
    if via == '25717:25635': # to河原町 はなぜかjsonのフォーマットが違う
        Departuretime_str = data["ResultSet"]["Course"]["Route"]["Line"][0]["DepartureState"]["Datetime"]["text"]
    else:
        Departuretime_str = data["ResultSet"]["Course"]["Route"]["Line"]["DepartureState"]["Datetime"]["text"]

    # 時刻の文字列を型変換する
    Date_str, time_add = Departuretime_str.split('T')
    Time_str, add = time_add.split('+')
    tstr = Date_str + ' ' + Time_str
    tdatetime = datetime.datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')

    # 結果を出力
    #print('====電車の表示====')
    #print('date and time = ', tdatetime)
    #print('hour = ', tdatetime.hour)
    #print('minute = ', tdatetime.minute)
    #print('second = ',tdatetime.second)
    #print('==電車の表示終わり==')

    return tdatetime, str(tdatetime.hour), str(tdatetime.minute), str(tdatetime.second)

if __name__ == '__main__':
    train_api()

