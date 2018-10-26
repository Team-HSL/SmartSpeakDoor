
import requests
import json


def weather_api(lat, lon):
    # APIキーの指定
    apikey = "fe57e94691b56f62072d40d52145cc30"

    # 天気を調べたい都市
    # city = "Tokyo"
    # lat = "35.68"
    # lon = "139.76"

    # APIのひな型
    # api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}" # Search by city name
    api = "http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&APPID={key}" # Search by location

    # 温度変換(ケルビン→摂氏)
    k2c = lambda k: k - 273.15

    # APIのURLを得る
    url = api.format(lat=lat, lon=lon, key=apikey)

    # 実際にAPIにリクエストを送信して結果を取得する
    r = requests.get(url)

    # 結果はJSON形式なのでデコードする
    data = json.loads(r.text)

    # 結果を出力
    #print('====天候の表示====')
    #print("+ 都市=", data["name"])
    #print("| 天気=", data["weather"][0]["description"])
    #print("| 最低気温=", k2c(data["main"]["temp_min"]))
    #print("| 最高気温=", k2c(data["main"]["temp_max"]))
    #print("| 湿度=", data["main"]["humidity"])
    #print("| 気圧=", data["main"]["pressure"])
    #print("| 風向き=", data["wind"]["deg"])
    #print("| 風速度=", data["wind"]["speed"])
    #print('==天候の表示終わり==')

    return data["weather"][0]["description"]

if __name__ == '__main__':
    weather_api()