from tkinter import *
from tkinter import ttk

def printValue():
    print(phone.get())
    print(home.instate(['selected']))


root = Tk()
phone = StringVar()

home = ttk.Radiobutton(root,text = 'Home',variable= phone,value='home',command=printValue)
office = ttk.Radiobutton(root,text='Office',variable=phone,value='office',command=printValue)
cell = ttk.Radiobutton(root,text='Cell',variable=phone,value='cell',command=printValue)

home.grid()
office.grid()
cell.grid()

root.mainloop()