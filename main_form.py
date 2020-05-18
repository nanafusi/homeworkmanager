import tkinter as tk
import sys
import time


def changeFrame(frame):
    # MainPageを上位層にする
    frame.tkraise()


def main_loop():
    root = tk.Tk()
    root.title(u"Kadai kanri")
    root.geometry("400x300")

    # メインフレームちそちそ
    mainFrame = tk.Frame(root)
    changeBtn = tk.Button(mainFrame, text="Goto Chiso Chiso",
                          command=lambda: changeFrame(tstsFrame))
    changeBtn.place(x=0,y=0)
    
    mainFrame.grid(row=0, column=0, sticky="nsew")
    
    
    

    # ちそちそフレーム
    tstsFrame = tk.Frame(root)
    #refer_btn = tk.Button(tstsFrame, text="課題参照", command=lambda: )
    #refer_btn.pack()
    Label = tk.Label(tstsFrame, text="ちそちそ")
    Label.pack()
    tstsFrame.grid(row=0, column=0)

    mainFrame.tkraise()

    root.mainloop()


main_loop()
