# -*- coding:utf-8 -*-
import tkinter as tk
from tkinter import filedialog, StringVar

class App(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        
        self.entry_src = tk.Entry()
        self.entry_src.pack()
        
        
        self.choose_src = tk.Button(text="选择原始文件目录")
        self.choose_src.bind('<ButtonPress>', self.choose_file)
        self.choose_src.setvar('DIR', None)
        self.choose_src.setvar('entry',self.entry_src)
        
        self.choose_src.pack()
    
        self.entry_dst = tk.Entry()
        self.entry_dst.pack()
        self.choose_dst = tk.Button(text="选择目标文件目录")
        self.choose_dst.bind('<ButtonPress>', self.choose_file)
        self.choose_dst.setvar('DIR', None)
        self.choose_dst.setvar('entry',self.entry_dst)
        self.choose_dst.pack()
        
      
        
        #self.pack()
    def choose_file(self,even):
       
        name = filedialog.askdirectory()
        even.widget.setvar('DIR',name)
        var = StringVar()
        var.set(name)
        print(type(even.widget.getvar('entry')))
        print(self.choose_src.getvar('DIR'))
        
        return 
    
        
    
if __name__ == '__main__':
    app = App()
    app.mainloop()