import sys
import tkinter
import cv2
import time
import os
import pandas as pd

#ここにメインの関数を入れる
def save():
    list_filename = './SmartSpeakDoorList.csv'
    SubjectList   = pd.read_csv(filepath_or_buffer=list_filename,header=0)
    num = len(SubjectList) # numは0-origin．新たに追加される人物のnum = 変更前の行数
    additionalData= pd.DataFrame([[num, name,city,departure, destination]],columns = SubjectList.columns)
    # additionalData= pd.DataFrame([[name,city,departure, destination]],columns = SubjectList.columns)
    SubjectList = SubjectList.append(additionalData)
    SubjectList.to_csv(list_filename,index=False,encoding='utf_8_sig')
    print('succeed', num, name, city,departure, destination)

def func_pic(event):
        global mode
        mode = 'picture'
        root.quit()

def imsave(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def picture():
    cap = cv2.VideoCapture(0)
    count = 0
    while(count < 3):
        while(True):
            ret, frame = cap.read()
            cv2.imshow('3 photos are needed. (Shutter : Space key)',frame)
            k = cv2.waitKey(1)
            if k == 32 : 
                break
        if not os.path.exists("./Face_img/" + name):
            os.mkdir("./Face_img/" + name)
        file_path = "./Face_img/" + name + "/Face_img_" + str(count) + ".jpg"
        imsave(file_path, frame)
        count += 1

    cap.release()
    cv2.destroyAllWindows()
def func_name(event):
    global Button5
    Button5 = tkinter.Button(text='決定', width=10)
    Button5.bind("<Button-1>",get_name)
    Button5.place(x=150, y=300)

    global EditBox 
    EditBox = tkinter.Entry()
    EditBox.place(x=100, y=240)
def get_name(event):
    global name 
    name = EditBox.get()
    EditBox.destroy()    
    Button5.destroy() 
def func_place(event):
    global Button6
    global Button7
    global Button8
    Button6 = tkinter.Button(text='大阪',width=10)
    Button6.bind("<Button-1>",osaka)
    Button6.place(x=50, y=300)
    Button7 = tkinter.Button(text='名古屋',width=10)
    Button7.bind("<Button-1>",nagoya)
    Button7.place(x=150, y=300)
    Button8 = tkinter.Button(text='東京',width=10)
    Button8.bind("<Button-1>",tokyo)
    Button8.place(x=250, y=300)
def func_station(event):
    global Button11
    global EditBox2 
    global EditBox3 
    EditBox2 = tkinter.Entry()
    EditBox2.insert(tkinter.END,"最寄駅")
    EditBox2.place(x=100, y=240)

    EditBox3 = tkinter.Entry()
    EditBox3.insert(tkinter.END,"目的地")
    EditBox3.place(x=100, y=300)

    Button11 = tkinter.Button(text='決定', width=5)
    Button11.bind("<Button-1>",get_station)
    Button11.place(x=160, y=340)

def osaka(event):
    global city
    city = 'osaka'
    Button6.destroy()    
    Button7.destroy() 
    Button8.destroy()
def nagoya(event):
    global city
    city = 'nagoya'
    Button6.destroy()    
    Button7.destroy() 
    Button8.destroy()
def tokyo(event):
    global city
    city = 'tokyo'
    Button6.destroy()    
    Button7.destroy() 
    Button8.destroy()
def get_station(event):
    global departure
    global destination 
    departure = EditBox2.get()
    destination = EditBox3.get()
    EditBox2.destroy()  
    EditBox3.destroy()   
    Button11.destroy() 
def finish(event):
    global mode
    mode = 'main'
    root.quit()


#初期値
name = 'ルネサス'
city = 'tokyo'
departure = '出町柳'
destination = '淀屋橋'
end = False

while end == False:
    
    root = tkinter.Tk()
    root.title("selection")
    root.geometry("400x400")


    Button2 = tkinter.Button(text='名前入力',width=20)
    Button2.bind("<Button-1>",func_name)
    Button2.place(x=100, y=0)

    Button3 = tkinter.Button(text='住んでる場所', width=20)
    Button3.bind("<Button-1>",func_place)
    Button3.place(x=100, y=60)

    Button4 = tkinter.Button(text='最寄駅', width=20)
    Button4.bind("<Button-1>",func_station)
    Button4.place(x=100, y=120)

    Button1 = tkinter.Button(text='写真撮影',width=20)
    Button1.bind("<Button-1>",func_pic)
    Button1.place(x=100, y=180)

    Button12 = tkinter.Button(text='入力完了', width=10)
    Button12.bind("<Button-1>",finish)
    Button12.place(x=150, y=300)


    root.mainloop()
    
    root.destroy()

    if mode == 'picture':
        picture()

    if mode == 'main':
        end = True
        save()