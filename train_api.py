
import requests
import json
import datetime

def train_api():

    # APIキーの指定
    apikey = "test_G2zn3qudefX"

    # 出発地の駅の名前
    station = "出町柳" # 出町柳code=25717

    # 目的地の駅の名前
    destination =  '河原町' # 河原町code=25635

    # 出発地と目的地の並列化
    via = '25717:25635'

    # 経路探索するためのURL
    api = "http://api.ekispert.jp/v1/json/search/course/extreme?key={key}&viaList={via}&answerCount=1"

    # 実際にAPIにリクエストを送信して結果を取得する
    url = api.format(key=apikey, via=via)
    r = requests.get(url)

    # 結果はJSON形式なのでデコードする
    data = json.loads(r.text)
    Departuretime_str = data["ResultSet"]["Course"]["Route"]["Line"][0]["DepartureState"]["Datetime"]["text"]

    # 時刻の文字列を型変換する
    Date_str, time_add = Departuretime_str.split('T')
    Time_str, add = time_add.split('+')
    tstr = Date_str + ' ' + Time_str
    tdatetime = datetime.datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')

    # 結果を出力
    print('====中身の表示====')
    print('date and time = ', tdatetime)
    print('hour = ', tdatetime.hour)
    print('minute = ', tdatetime.minute)
    print('second = ',tdatetime.second)
    print('==中身の表示終わり==')

    return tdatetime, tdatetime.hour, tdatetime.minute, tdatetime.second

if __name__ == '__main__':
    train_api()

