import sqlite3 as sq
import os
from datetime import datetime as dt
import sys
import tkinter as tk
import time

Timetable = ["電子回路２", "応用数学１", "発変電工学", "英語", "第二外国語", "情報通信", "数値解析", "電子工学",
             "日本経済論", "保健体育", "電気磁気学", "応用数学２", "回路網理論", "ＤＢ論"]

dbpath = 'kadais.sqlite'

tmp_key = 9999

# 自動でDBにcommitされる

connection = sq.connect(dbpath, isolation_level=None)

cursor = connection.cursor()


def initialize():
    try:
        # CREATE
        # なぜかなかったら新しく作る
        # connectの段階でデータベースファイルは生成されるから注意
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS todo(class integer, date text, about text, key integer primary key)")
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])


def check_format(sdate):
    # 日付のフォーマットをチェックする
    try:
        fdate = dt.strptime(sdate, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


def todo_view():
    print("\n現在の予定はこちらです")
    print("{} {} {} {}".format("ID", "教科".ljust(5, "　"), "期限".ljust(17), "概要"))
    print("-"*60)
    for row in cursor.execute("SELECT * FROM todo ORDER BY date ASC"):
        print("{} {} {} {}".format(
            row[3], Timetable[int(row[0])].ljust(5, "　"), row[1], row[2]))
    print("")


def todo_order_key():
    try:
        cursor.execute(
            "UPDATE todo AS a SET key = ("
            "SELECT rank FROM ("
            "SELECT rowid AS row_id, ROW_NUMBER() OVER(ORDER BY date ASC) AS rank "
            "FROM todo) AS b WHERE b.row_id=a.rowid)")
    except sqlite3.Error as e:
        print("KEYの並び替えに失敗しました: ", e.args[0])


def todo_add():
    print("\n課題を追加したい教科を選択してください(数字)")

    for index, t in enumerate(Timetable):
        print(str(index) + " " + t)
    print("\n> ", end="")

    ans_class = str(input())

    while True:
        print("提出期限を右の書式通りに入力してください(yyyy-mm-dd hh:mm:ss)> ", end="")
        ans_date = str(input())
        if check_format(ans_date):
            break
        else:
            print("フォーマットエラー")

    print("概要を入力してください> ", end="")
    ans_about = str(input())

    print("")
    print("教科: " + Timetable[int(ans_class)])
    print("日付: " + ans_date)
    print("概要: " + ans_about)

    while True:
        print("これでよろしいですか？(Y/N/C)> ", end="")
        chk = str(input())
        if chk.lower() == "Y".lower():
            # 追加する
            try:
                # INSERT
                cursor.execute("INSERT INTO todo VALUES (?, ?, ?, ?)",
                               (ans_class, ans_date, ans_about, tmp_key))
                # ここで連番振り直し
                todo_order_key()
                print("追加しました\n")
            except sq.Error as e:
                print("追加に失敗しました("+e.args[0]+")\n")
            break
        elif chk.lower() == "N".lower():
            # やり直し
            return todo_add()
        elif chk.lower() == "C".lower():
            # キャンセル
            print("\n")
            return


def todo_del():
    print("\n削除する予定IDを入力してください")
    print("{} {} {} {}".format("ID", "教科".ljust(5, "　"), "期限".ljust(17), "概要"))
    print("-"*60)
    for row in cursor.execute("SELECT * FROM todo ORDER BY date ASC"):
        print("{} {} {} {}".format(
            row[3], Timetable[int(row[0])].ljust(5, "　"), row[1], row[2]))
    print("")

    print("> ", end="")
    ans_id = int(input())

    print("\n削除する予定はこれでよろしいですか")
    for row in cursor.execute("SELECT * FROM todo WHERE key = ?", (ans_id,)):
        print("{} {} {} {}".format(
            row[3], Timetable[int(row[0])].ljust(5, "　"), row[1], row[2]))


def end():
    connection.commit()
    connection.close()
    sys.exit(0)


def changeFrame(frame):
    # MainPageを上位層にする
    frame.tkraise()


def form_loop():
    root = tk.Tk()
    root.title(u"Kadai kanri")
    root.geometry("400x300")

    # メインフレームちそちそ
    mainFrame = tk.Frame(root)
    change_Btn = tk.Button(mainFrame, text="課題編集", command=lambda: todo_add())
    change_Btn.pack()

    refer_Btn = tk.Button(mainFrame, text="課題参照", command=lambda: todo_view())
    refer_Btn.pack()

    exit_Btn = tk.Button(mainFrame, text="終了", command=lambda: end())
    exit_Btn.pack()

    mainFrame.grid(row=0, column=0, sticky="nsew")

    # ちそちそフレーム
    # tstsFrame = tk.Frame(root)
    # tstsLabel = tk.Label(tstsFrame, text="ちそちそ")
    # tstsLabel.pack()
    # tstsFrame.grid(row=0, column=0, sticky="nsew")

    mainFrame.tkraise()

    root.mainloop()


while True:
    initialize()
    # form_loop()
    print("課題管理プログラム\n1 課題予定追加, 2 課題予定参照, 3 課題予定削除, 99 終了> ", end="")

    answer = str(input())
    if answer == "1":
        todo_add()

    elif answer == "2":
        todo_view()

    elif answer == "3":
        todo_del()

    elif answer == "99":
        end()
