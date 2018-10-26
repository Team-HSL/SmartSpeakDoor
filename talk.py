
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
        sleep(4)

if __name__ == '__main__':

    import sys
    sys.path.append('./api_code')

    from api import api
    name, train, weather, schedule = api(2) # 1 or 2 can be used.
    talk_list = [name, train, weather, schedule]
    talk(talk_list)


