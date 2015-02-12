from tkinter import *
from tkinter import ttk

def printText(event):
    
    print(strVar.get())
    


root = Tk()

strVar = StringVar()
country = ttk.Combobox(root,textvariable=strVar,state='readonly')

country.bind('<<ComboboxSelected>>', printText)
country['values'] = ('USA', 'Canada', 'Australia')
country.current(1)
country.grid()

root.mainloop()