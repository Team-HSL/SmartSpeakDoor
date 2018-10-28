def talk(talklist):

    import sys
    import os
    import subprocess
    from time import sleep
    import winsound
    sys.path.append('./api_code')
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

    os.system('rd /s /q directory')
    os.system('mkdir ja_sound')
    for i, x in enumerate(talklist):
        jtalk(x.encode('shift-jis'), i)
        # sleep(3)

if __name__=="__main__":
    talk(["村木たつやさんの今日の予定は，ショッピングです電車は最終"])