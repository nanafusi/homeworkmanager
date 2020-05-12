from ctypes import *
import os 
import json
import collections as cl
import datetime

date_list = ["月","火","水","木","金"]

Timetable = ["電子回路２","応用数学１","発変電工学","なし","英語","第二外国語","情報通信","数値解析","電子工学","ニッポン経済論","保健体育","なし","電気磁気学","応用数学２","第二外国語","なし","回路網理論","データベース論","電子工学","なし"]

initialize = os.path.isfile("plans.json")
if not initialize:
    with open("plans.json","w") as f:
        print("[*]plans.json is not found! creating....")
        ys = cl.OrderedDict()
        for i in range(len(date_list)):
            
           data = cl.OrderedDict()

           for j in range(i*4,(i+1)*4):
               data[Timetable[j]] = "課題なし"

           ys[date_list[i]] = data
        json.dump(ys,f,indent=4)
        print("[*]plans.json was created!")

def refer_plans(json_data):
    
    for i in date_list:
        print("{}曜日".format(i))
        for j in range(0,4):
            print("{} : {}".format(list(json_data[i].keys())[j] , json_data[i][list(json_data[i].keys())[j]]))
        print(" ")

def change_plans(json_data):
    print("どの曜日の教科を編集しますか？ 0 月曜日　1 火曜日　2 水曜日 3 木曜日 4 金曜日")
    answer = int(input())
    for j in range(0,4):
            print("{} : {}".format(list(json_data[date_list[answer]].keys())[j] , json_data[date_list[answer]][list(json_data[date_list[answer]].keys())[j]]))

    print("どの科目を編集しますか? 上から 0 1 2 3")

    subject = int(input())

    print("課題を入力してください")

    homework = str(input())
    json_data[date_list[answer]][list(json_data[date_list[answer]].keys())[subject]] = homework
    with open("plans.json","w") as f:
        json.dump(json_data,f,indent=4)
    

while True:


    print("課題管理プログラム: 入力してください 1 課題予定追加 2 課題予定参照 3 通期機能ONOFF")

    answer = str(input())
    if answer == "1":
       with open("plans.json","r") as d:

           json_data = json.load(d)

           change_plans(json_data)

    elif answer == "2":
        with open("plans.json","r") as d:
           json_data = json.load(d)

           refer_plans(json_data)

    elif answer == "3":
        set_frag()
