from tkinter import *
from tkinter import ttk

def printOK():
    print (checkbutton.instate(['selected']))
    print(strVar.get())

root = Tk()
strVar = StringVar()
checkbutton = ttk.Checkbutton(root,text='check',command = printOK,variable=strVar,onvalue='Check',offvalue='UnCheck')

checkbutton.grid()
print (checkbutton.instate(['selected']))

root.mainloop()

