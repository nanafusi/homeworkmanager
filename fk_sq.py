import sqlite3 as sq

dbpath = 'kadais.sqlite'

connection = sq.connect(dbpath)
cursor = connection.cursor()

try:
    # CREATE
    #cursor.execute("DROP TABLE IF EXISTS todo")
    # dateの書式：yyyy-mm-dd hh:mm:ss
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS todo (class integer, date text, about text)")
except sqlite3.Error as e:
    print('sqlite3.Error occurred:', e.args[0])


def todo_view():
    for row in cursor.execute("SELECT * FROM todo"):
        print(row)


def end():
    connection.commit()
    connection.close()
    exit()


while True:

    print("課題管理プログラム\n1 課題予定追加, 2 課題予定参照, 3 通期機能ONOFF, 99 終了")

    answer = str(input())
    if answer == "1":
        print("add")

    elif answer == "2":
        print("view")
        todo_view()

    elif answer == "3":
        print("set notif")

    elif answer == "99":
        end()
