
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


if __name__ == '__main__':
    import sys
    sys.path.append('./api_code')
    api(1)
    # api(2)

