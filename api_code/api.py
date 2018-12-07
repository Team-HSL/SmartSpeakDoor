import datetime
from weather_api import weather_api
from train_api import train_api
from calender_api import calender_api

def api(params):
    '''
    params : dict_key [name,start,finish,city]
    '''
    calenderID = '8e5etm3bvc22pgjj60795lel2s@group.calendar.google.com' # Goto ID
    name  = params['name']
    start = params['departure']
    finish= params['destination']

    # city parameters (緯度と経度)
    if params['city'] == '大阪':
        lat = '34.70'
        lon = '135.49'

    elif params['city'] =='東京':
        lat = '35.70'
        lon = '139.73'
    else :
        lat = '35.17'
        lon = '136.88'

    name = name + "さん"
    tdatetime, hour, minute, second = train_api(start, finish) # tdatetime is date. others are str.
    weather = weather_api(lat, lon)
    eventlist = []
    # eventlist, startlist = calender_api(calenderID) # list returned
    currenttime = datetime.datetime.now()
    u = tdatetime - currenttime
    
    tmp = u.seconds//60

    # 発車時刻ちょうどに実行すると，tmpの結果が 24*60 - 1 分くらいになってしまう．
    # この時だけ除外する処理を行う．
    if tmp == 1439:
        print("やばい")
        tmp = 0
    tmp = str(tmp)

    train = hour + '時' + minute + '分' + 'に発車します。' + 'あと' + tmp + '分で発車します。'
    weather = '今日の' + params['city'] + 'の天気は' + weather + 'です。'
    
    if len(eventlist) == 0:
        schedule = '予定はありません．' 
    else:
        schedule = '予定は' + eventlist[0] + 'があります。'
    
    # these lines will be deleted.
    print(name)
    print(train)
    print(weather)

    return name, train, weather, schedule

if __name__ == '__main__':
    params = {'name':'後藤','start':'出町柳','finish':'淀屋橋','city':'osaka'}
    api(params)
    # api(2)
