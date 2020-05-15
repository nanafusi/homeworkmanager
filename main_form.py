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
    changeBtn.pack()
    mainFrame.grid(row=0, column=0, sticky="nsew")

    # ちそちそフレーム
    tstsFrame = tk.Frame(root)
    tstsLabel = tk.Label(tstsFrame, text="ちそちそ")
    tstsLabel.pack()
    tstsFrame.grid(row=0, column=0, sticky="nsew")

    mainFrame.tkraise()

    root.mainloop()


main_loop()
