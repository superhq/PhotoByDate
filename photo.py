# -*- coding:utf-8 -*-
# Python >= 3.3
import os
import datetime
import shutil
from exif_info import *

def list_regular_files(path):
    """
    list all files in the directory and the sub-directories
    """
    for item in os.listdir(path):
        name= os.path.join(path,item)
        try:
            if os.path.isdir(name):
                yield from list_regular_files(name)
            else:
                yield name
        except Exception as e:
            print(e)
def is_path_correct(path1,path2):
    if path1 in path2:
        print('%s is sub of %s'%(path2,path1))
    elif path2 in path1:
        print('%s is sub of %s'%(path1,path2))
    else:
        print('ok')
    

def parse_regular_file(src,dst_path):
    """
    """

    (folder_name,dst_name) = get_original_time(src)
    folder_path = os.path.join(dst_path,folder_name)
    if os.path.isdir(folder_path) is False:
        print("create %s"%(folder_path))
        os.makedirs(folder_path)
        
    dst = os.path.join(folder_path,dst_name)
    print("copy[%s]to[%s]"%(src,dst))
    
    #拷贝文件及属性
    shutil.copy2(src,dst)
    
    #拷贝文件
    #shutil.copyfile(src, dst)
    #拷贝属性
    #shutil.copystat(src, dst)
    

if __name__ == '__main__':
     i = 0
     for name in list_regular_files('E:\\'):
         parse_regular_file(name,'F:\\照片--分类后')
         i = i + 1
     print("一共有%d个文件"%(i,))
    #is_path_correct('E:\ipad20141227','F:\python-work\Camera\\test')
        
        
    