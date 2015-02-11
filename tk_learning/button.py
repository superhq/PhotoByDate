from tkinter import *
from tkinter import ttk

def printok():
    print('OK')


root = Tk()

image = PhotoImage(file='image.gif')

button = ttk.Button(root,text='OK',image=image,compound='center',command=printok)

button.grid()

root.mainloop()