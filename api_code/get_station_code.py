
import requests
import json
import datetime


def get_station_code(Station):  # 'Station' must be string.

    # APIキーの指定
    with open('./api_code/keys/trainAPIkey.txt') as f:
        apikey = f.read()

    # 駅コードを取得するためのURL
    api = "http://api.ekispert.jp/v1/json/station/light?key={key}&name={station}&type=train"

    # 実際にAPIにリクエストを送信して結果を取得する
    url = api.format(key=apikey, station=Station)
    r = requests.get(url)

    # 結果はJSON形式なのでデコードする
    data = json.loads(r.text)

    try:
        number = data['ResultSet']['Point'][0]['Station']['code']
    except KeyError:
        number = data['ResultSet']['Point']['Station']['code']

    return number


if __name__ == '__main__':
    get_station_code('新宿三丁目')
