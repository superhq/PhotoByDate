# -*- coding:utf-8 -*-

import os
import datetime
from exifread import process_file

def get_original_time2(name):
    basename = os.path.basename(name)
    #得到修改时间
    t =  os.path.getmtime(name)
    dt = datetime.datetime.fromtimestamp(t)
    f = open(name,'rb')
    tags = process_file(f,stop_tag='EXIF DateTimeOriginal')
    
    if 'EXIF DateTimeOriginal' in tags:
    #得到拍摄时间，如2006:12:08 18:50:45，进行格式化，并加入毫秒数
        dt_original = str(tags['EXIF DateTimeOriginal'])
        (_d,_t) = (dt_original.split())
        _d = _d.replace(':','-')
        _t = _t.replace(':','')
        prefix="%s %s"%(_d,_t)
        (year,month,day) = _d.split('-')
        folder_name="%s-%s"%(year,month)
        
    #如果没有拍摄时间，则以修改时间代替
    else:
        prefix = ("%d-%02d-%02d %02d%02d%02d")%\
        (dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)
        folder_name="%d-%02d"%(dt.year,dt.month)
    return (folder_name,prefix+'--'+basename)

def get_original_time(name):
    #得到修改时间
    t =  os.path.getmtime(name)
    #得到创建时间
    #t = os.path.getctime(name)
    dt = datetime.datetime.fromtimestamp(t)
    #得到文件类型
    ftype =  os.path.splitext(name)[1]
    
    f = open(name,'rb')
    tags = process_file(f,stop_tag='EXIF DateTimeOriginal')
    
    if 'EXIF DateTimeOriginal' in tags:
    #得到拍摄时间，如2006:12:08 18:50:45，进行格式化，并加入毫秒数
        dt_original = str(tags['EXIF DateTimeOriginal'])
        (_d,_t) = (dt_original.split())
        _d = _d.replace(':','-')
        _t = _t.replace(':','')
        dst_name="%s %s_%d%s"%(_d,_t,dt.microsecond,ftype)
        (year,month,day) = _d.split('-')
        folder_name="%s-%s"%(year,month)
        
    #如果没有拍摄时间，则以修改时间代替
    else:
        dst_name = ("%d-%02d-%02d %02d%02d%02d_%d%s")%\
        (dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,dt.microsecond,ftype)
        folder_name="%d-%02d"%(dt.year,dt.month)

    return (folder_name,dst_name)
if __name__ == '__main__':
    print(get_original_time('./1.jpg'))
    #print(get_original_time('./source.jpeg'))