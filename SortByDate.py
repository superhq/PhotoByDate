#-*- encoding:utf8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from functools import partial
import threading
import sys
import time
import os
#from tkinter.test.runtktests import is_package
from exif_info import *
from imp import new_module
import shutil

g_flag = None
g_lock = threading.Lock()

class ProcessPhoto(threading.Thread):
    def __init__(self,output_fun,end_fun,update_progress,src,dest):
        threading.Thread.__init__(self)
        self.output_fun = output_fun
        self.end_fun = end_fun
        self.update_progress = update_progress
        
        self.src = src
        self.dest = dest
        
        
        
    def run(self):
        self.rename()
        self.end_fun()
    def rename(self):
        self.max = sum(1 for x in self.list_regular_files(self.src))
        self.count = 0
        for name in self.list_regular_files(self.src):
            g_lock.acquire()
            flag = g_flag
            g_lock.release()
            while flag == MainUI.SUSPEND:
                time.sleep(0.1)
                g_lock.acquire()
                flag = g_flag
                g_lock.release()
            if flag == MainUI.STOP:
                break
           
            self.count = self.count + 1
            self._rename(name)
            self.update_progress(self.count,self.max)
            
    def _rename(self,name):
        (folder,fname) = get_original_time2(name)
        dest_folder = os.path.join(self.dest,folder)
        if os.path.isdir(dest_folder) is False:
            self.output_fun('创建文件夹:%s'%(dest_folder))
            os.makedirs(dest_folder)
        new_name = os.path.join(dest_folder,fname)
        src_name = os.path.join(self.src,name)
        
        #拷贝文件及属性
        shutil.copy2(src_name,new_name)
        self.output_fun('[%d/%d] 拷贝 %s 到  %s'%(self.count,self.max,src_name,new_name))
            
    def list_regular_files(self,path):

        for item in os.listdir(path):
            name= os.path.join(path,item)
            try:
                if os.path.isdir(name):
                    yield from self.list_regular_files(name)
                else:
                    yield name
            except Exception as e:
                self.output_fun(str(e))
            


class MainUI():
    BEGIN = 1
    SUSPEND = 2
    STOP = 3
    def __init__(self):

        self.root = Tk()
        self.src_text = StringVar()
        self.dest_text = StringVar()
        
        self.content = ttk.Frame(self.root)
        self.lab1 = ttk.Label(self.content,text = '待处理:')
        self.lab2 = ttk.Label(self.content,text = '处理到:')
        self.src = ttk.Entry(self.content,textvariable = self.src_text,state='readonly')
        self.dest = ttk.Entry(self.content,textvariable= self.dest_text,state='readonly')
        self.src_selector = ttk.Button(self.content,text = '...', command = partial(self.choose_dir,self.src_text))
        self.dest_selector = ttk.Button(self.content,text = '...', command = partial(self.choose_dir,self.dest_text))
        self.progress = ttk.Progressbar(self.content)
        self.begin = ttk.Button(self.content,text = '开始',command = partial(self.operator,MainUI.BEGIN))
        self.suspend = ttk.Button(self.content,text='暂停',command = partial(self.operator,MainUI.SUSPEND))
        self.stop = ttk.Button(self.content,text = '停止',command = partial(self.operator,MainUI.STOP))
        self.info = Text(self.content,wrap="none",state=DISABLED)
        
        self.yscroll = ttk.Scrollbar(self.content,orient=VERTICAL, command=self.info.yview)
        self.xscroll = ttk.Scrollbar(self.content,orient=HORIZONTAL,command=self.info.xview)
        self.info['yscrollcommand'] = self.yscroll.set
        self.info['xscrollcommand'] = self.xscroll.set
        
        self.content.grid(column = 0, row = 0, sticky = (N,S,E,W)) 
        self.lab1.grid(column = 0,row = 0)
        self.src.grid(column = 1, row = 0, columnspan = 3,sticky=(E,W))
        self.src_selector.grid(column = 4, row = 0)  
        self.lab2.grid(column = 0 , row = 1)
        self.dest.grid(column = 1, row = 1, columnspan = 3,sticky=(E,W))
        self.dest_selector.grid(column = 4, row = 1)
        self.progress.grid(column = 0, row = 2, columnspan = 2,sticky=(E,W))
        self.progress.grid_remove()
        
        self.begin.grid(column = 2, row = 2)
        self.suspend.grid(column = 3, row = 2)
        self.stop.grid(column = 4, row = 2)
        self.info.grid(column = 0, row = 3, columnspan = 5, rowspan = 5,sticky=(N,S,E,W))
        self.yscroll.grid(column = 5, row = 3,rowspan = 5,sticky=(N,S))
        self.xscroll.grid(column = 0, row = 8,columnspan = 5, sticky=(W,E))
        
        self.root.columnconfigure(0, weight = 1)
        self.root.rowconfigure(0, weight = 1)
        self.content.columnconfigure(0,weight = 0)
        self.content.columnconfigure(1,weight = 1)
        self.content.columnconfigure(2,weight = 0,pad = 3)
        self.content.columnconfigure(3,weight = 0,pad = 3)
        self.content.columnconfigure(4,weight = 0,pad = 3)
        self.content.rowconfigure(0,weight = 0,pad = 5)
        self.content.rowconfigure(1,weight = 0,pad = 5)
        self.content.rowconfigure(2,weight = 0,pad = 5)
        self.content.rowconfigure(3,weight = 1)
        self.content.rowconfigure(4,weight = 1)
        self.content.rowconfigure(5,weight = 1)
        self.content.rowconfigure(6,weight = 1)
        self.content.rowconfigure(7,weight = 1)
        
        self.begin.state(['disabled'])
        self.suspend.state(['disabled'])
        self.stop.state(['disabled'])
        
        
        self.thread_rename = None
        global g_flag #declare global variable if we need to modify it
        g_flag = None

        
        
        
        
        
    def choose_dir(self,text):
        path = filedialog.askdirectory()
        text.set(path)
        if self.src_text.get() != '' and self.dest_text.get() != '':
            if self.is_path_correct(self.src_text.get(),self.dest_text.get()):
                self.begin.state(['!disabled'])
            else:
                self.output_info('请重新选择输出目录')
            
            
    def is_path_correct(self,path1,path2):
        if path1 in path2:
            return False
        elif path2 in path1:
            return False
        else:
            return True
    
     
       
    def operator(self,OPT):
        global g_flag #declare global variable if we need to modify it
        if OPT == MainUI.BEGIN:
            
            self.begin.state(['disabled'])
            self.suspend.state(['!disabled'])
            self.stop.state(['!disabled'])
            self.src_selector.state(['disabled'])
            self.dest_selector.state(['disabled'])
            
            self.progress.grid()
            
            
            
            g_lock.acquire()
            g_flag = MainUI.BEGIN
            g_lock.release()
            
            if self.thread_rename == None:
                self.thread_rename = ProcessPhoto(self.output_info,self.end_fun,\
                                                  self.update_progress,self.src_text.get(),self.dest_text.get())
                self.thread_rename.start()
            
  
        elif OPT == MainUI.SUSPEND:
            #print('suspend')
            self.begin.state(['!disabled'])
            self.suspend.state(['disabled'])
            self.stop.state(['!disabled'])
            g_lock.acquire()
            g_flag = MainUI.SUSPEND
            g_lock.release()
            
        elif OPT == MainUI.STOP:
            #print('stop')
            self.begin.state(['!disabled'])
            self.suspend.state(['disabled'])
            self.stop.state(['disabled'])
            self.src_selector.state(['!disabled'])
            self.dest_selector.state(['!disabled'])
            g_lock.acquire()
            g_flag = MainUI.STOP
            g_lock.release()
            
            #self.thread_rename.join()
        else:
            pass
        
    def end_fun(self):
        self.thread_rename = None
        self.begin.state(['!disabled'])
        self.suspend.state(['disabled'])
        self.stop.state(['disabled'])
        self.src_selector.state(['!disabled'])
        self.dest_selector.state(['!disabled'])
        self.progress.grid_remove()
        
    def update_progress(self,v,max):
        self.progress.config(maximum=max)
        self.progress.config(value=v)
        
    
    def output_info(self,text):
        self.info.config(state=NORMAL)
        self.info.insert('end', text + '\n')
        self.info.yview('end')
        self.info.config(state=DISABLED)
        

        
        
            
    
        
        
    def mainloop(self):
        self.root.mainloop()
        

if __name__ == '__main__':
    mainui = MainUI()
    mainui.mainloop()