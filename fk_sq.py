import sqlite3 as sq
import os
from datetime import datetime as dt
import sys
import tkinter as tk
import tkinter.ttk as ttk
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
            "CREATE TABLE IF NOT EXISTS todo(class text, date text, about text, key integer primary key)")
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])


def check_format(sdate):
    # 日付のフォーマットをチェックする
    try:
        fdate = dt.strptime(sdate, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False


def todo_view():
    print("\n現在の予定はこちらです")
    print("{} {} {} {}".format("ID", "教科".ljust(5, "　"), "期限".ljust(17), "概要"))
    print("-"*60)
    for row in cursor.execute("SELECT * FROM todo ORDER BY date ASC"):
        print("{} {} {} {}".format(
            str(row[3]).rjust(2,' '), row[0].ljust(5, "　"), row[1], row[2]))
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
        print("提出期限を右の書式通りに入力してください(yyyy-mm-dd hh:mm)> ", end="")
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
                               (Timetable[int(ans_class)], ans_date, ans_about, tmp_key))
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
            row[3], row[0].ljust(5, "　"), row[1], row[2]))
    print("")

    print("> ", end="")
    ans_id = int(input())

    print("\n削除する予定はこれでよろしいですか")
    for row in cursor.execute("SELECT * FROM todo WHERE key = ?", (ans_id,)):
        print("{} {} {} {}".format(
            row[3], row[0].ljust(5, "　"), row[1], row[2]))


def end():
    connection.commit()
    connection.close()
    sys.exit(0)


def changeFrame(frame):
    # MainPageを上位層にする
    frame.tkraise()


def reload_tree(tree):
    i=0
    tree.delete(*tree.get_children())
    for r in cursor.execute("SELECT class,date,about FROM todo ORDER BY date ASC"):
        tree.insert("","end",tags=i,values=r)
        if i&1:
            tree.tag_configure(i,background="#CCFFFF")
        i+=1


def form_loop():
    root = tk.Tk()
    root.title(u"Kadai kanri")
    root.geometry("333x300")
    root.resizable(width=False, height=False)

    # メインフレームちそちそ
    f0 = tk.Frame(root)
    f1=tk.Frame(root)

    # ツリービュー
    kadai_tree=ttk.Treeview(root)
    kadai_tree["columns"]=(1,2,3)
    kadai_tree["show"]="headings"
    kadai_tree.column(1,width=70)
    kadai_tree.column(2,width=100)
    kadai_tree.column(3,width=150)
    kadai_tree.heading(1,text="教科")
    kadai_tree.heading(2,text="期限")
    kadai_tree.heading(3,text="概要")

    reload_tree(kadai_tree)

    kadai_tree.pack(in_=f1,fill=tk.BOTH)#grid(row=3,column=0,padx=5,pady=5,sticky=tk.W + tk.E)

    # ボタンの配置
    change_Btn = tk.Button(f0, text="課題追加", command=lambda: todo_add()).pack(side=tk.LEFT)
    #change_Btn.grid(row=0,column=0,padx=5)
    
    refer_Btn = tk.Button(f0, text="課題更新", command=lambda: reload_tree(kadai_tree)).pack(side=tk.LEFT)
    #refer_Btn.grid(row=0,column=1,padx=5)

    delete_Btn = tk.Button(f0, text="課題削除", command=lambda: todo_del()).pack(side=tk.LEFT)
    #delete_Btn.grid(row=0,column=2,padx=5)

    exit_Btn = tk.Button(root, text="終了", command=lambda: end()).pack(in_=f1,fill=tk.BOTH)
    #exit_Btn.grid(row=1,column=0,columnspan=3,padx=5,pady=5,sticky=tk.W + tk.E)

    # フレームの配置(いらんと思う)
    f0.pack()
    f1.pack()

    root.mainloop()

initialize()
form_loop()
while True:
    #print("課題管理プログラム\n1 課題予定追加, 2 課題予定参照, 3 課題予定削除, 99 終了> ", end="")

    #answer = str(input())
    #if answer == "1":
    #    todo_add()

    #elif answer == "2":
    #    todo_view()

    #elif answer == "3":
    #    todo_del()

    #elif answer == "99":
    #    end()
    pass
