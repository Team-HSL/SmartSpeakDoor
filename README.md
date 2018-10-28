# Smart Speak Door

## 必要なパッケージ・pythonライブラリ等(Windows10)

- AnacondaでTensorflow用の仮想環境(python=3.5)
- tensorflow(ver1.10 or Later)
- [tensorflow models][1]
- [pyserial][2]
- [google api python client][3]
- [Open J-talk][4]
- [cognitive face][5]

## 準備

コマンドプロンプトか何かでPATHの登録
```
set PYTHONPATH=[path to models]/models;[path to models]/models/research;[path to models]/models/research/slim
```

```
set PATH=%PATH%;PYTHONPATH
```



[1]:https://github.com/tensorflow/models
[2]:https://pythonhosted.org/pyserial/
[3]:https://github.com/googleapis/google-api-python-client
[4]:http://open-jtalk.sp.nitech.ac.jp/
[5]:https://github.com/Microsoft/Cognitive-Face-Python