from tkinter import *
from tkinter import ttk

#create root
root = Tk()

#create container
frame = ttk.Frame(root)
frame.grid()

#create lable
lable = ttk.Label(frame,text='Hello World')
lable.grid()

#widget monitor
strVar = StringVar()
lable['textvariable'] = strVar
strVar.set('Hello')

#set image
image = PhotoImage(file='image.gif')
lable['image'] = image

#show image and text
lable['compound'] = 'top'
#main loop
root.mainloop()