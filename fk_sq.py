import sqlite3 as sq
import os
from datetime import datetime as dt

Timetable = ["電子回路２", "応用数学１", "発変電工学", "英語", "第二外国語", "情報通信", "数値解析", "電子工学",
             "日本経済論", "保健体育", "電気磁気学", "応用数学２", "回路網理論", "ＤＢ論"]

dbpath = 'kadais.sqlite'

# 自動でDBにcommitされる
connection = sq.connect(dbpath, isolation_level=None)
cursor = connection.cursor()

try:
    # CREATE
    # なぜかなかったら新しく作る
    if not os.path.isfile(dbpath):
        print("データベースが存在しません。新たに作成します。")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS todo (class integer, date text, about text)")
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
    print("{} {} {}".format("教科".ljust(5, "　"), "期限".ljust(17), "概要"))
    print("-"*60)
    for row in cursor.execute("SELECT * FROM todo ORDER BY date ASC"):
        print("{} {} {}".format(
            Timetable[int(row[0])].ljust(5, "　"), row[1], row[2]))
    print("")


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
                cursor.execute("INSERT INTO todo VALUES (?, ?, ?)",
                               (ans_class, ans_date, ans_about))
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


def end():
    connection.commit()
    connection.close()
    exit()


while True:

    print("課題管理プログラム\n1 課題予定追加, 2 課題予定参照, 3 通期機能ONOFF, 99 終了> ", end="")

    answer = str(input())
    if answer == "1":
        todo_add()

    elif answer == "2":
        todo_view()

    elif answer == "3":
        print("set notif")

    elif answer == "99":
        end()
