from tkinter import *
from tkinter import ttk
#read:http://www.tkdocs.com/tutorial/concepts.html

#callback function
def change_text(event):
    
    if event.type == '7':
        event.widget['text'] = 'Enter'
    elif event.type == '8':
        event.widget['text'] = 'Leave'
    elif event.type == '4':
        event.widget['text'] = 'OK'
    

#1. create root window
root = Tk()

#2. create button widget
button = ttk.Button(root,text='Hello World')

#3. bind event
button.bind('<Enter>', change_text)
button.bind('<Leave>', change_text)
button.bind('<ButtonPress>',change_text)



#4. geometry management
button.grid()

#5. main loop
root.mainloop()

