import tkinter as tk
import sys
import time
from fk_sq import *

def changeFrame(frame):
    # MainPageを上位層にする
    frame.tkraise()


def main_loop():
    root = tk.Tk()
    root.title(u"Kadai kanri")
    root.geometry("400x300")

    # メインフレームちそちそ
    mainFrame = tk.Frame(root)
    change_Btn = tk.Button(mainFrame, text="課題編集",
                          command=lambda: fk_sq.todo_add())
    change_Btn.pack()
    refer_Btn = tk.Button(mainFrame, text="課題参照",command=lambda: fk_sq.todo_view())
    refer_Btn.pack()
    mainFrame.grid(row=0, column=0, sticky="nsew")

    ## ちそちそフレーム
    #tstsFrame = tk.Frame(root)
    #tstsLabel = tk.Label(tstsFrame, text="ちそちそ")
    #tstsLabel.pack()
    #tstsFrame.grid(row=0, column=0, sticky="nsew")

    mainFrame.tkraise()

    root.mainloop()

