from tkinter import *
from tkinter import ttk

def printText():
    print(strVar.get())
    return 1

def printText2():
    print(strVar.get())
    return 0
    

root = Tk()
strVar = StringVar()
#entry = ttk.Entry(root,textvariable=strVar,show='*')
#entry = ttk.Entry(root,textvariable=strVar,state='disable')
entry = ttk.Entry(root,textvariable=strVar,validatecommand=printText,invalidcommand =printText2,validate='all')

entry.grid()

root.mainloop()