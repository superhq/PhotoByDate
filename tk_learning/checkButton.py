from tkinter import *
from tkinter import ttk

def printOK():
    print (checkbutton.instate(['selected']))

root = Tk()
strVar = StringVar()
checkbutton = ttk.Checkbutton(root,text='check',command = printOK)

checkbutton.grid()
print (checkbutton.instate(['selected']))

root.mainloop()

