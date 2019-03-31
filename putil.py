#coding=utf-8
#设计转换函数
from workf.settings import BASE_DIR
import re,os
base=2**10#基数1024
units={0:'b',1:'kb',2:'mb',3:'gb',4:'tb'}#常用字节大小单位字典
count=0
#coding=utf-8
#转换时间
import time
#转换为时间戳
def tr_1(date_str):
    date = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")#转换成tuple日期
    stamp = int(time.mktime(date))
    return stamp
#转换为str格式的时间
def tr_2(stamp):
    date= time.localtime(stamp)#转换成tuple日期
    return time.strftime("%Y-%m-%d %H:%M:%S", date)
def transfer_h(value):
    def transfer(value1):
        global count
        v=value1 // base
        if v>0:
            count+=1
            transfer(v)
        else:pass
    value1=int(value.strip("bB"))#将单位字符去掉转换成int
    transfer(value1)#确认转换单位
    msg="{} {}".format(str(float(value1)/pow(base,count)),units[count])#输出转换单位值
    return msg


def transfer_b(value):
    unit=re.search(r'\D+',value).group(0)#提取字节大小单位
    d=int(value.strip(unit))#提取数值
    for k,v in units.items():
        if unit.lower() in v:
            return d * pow(base,k)#转换成单位为b的大小




def logger(msg):
    t=tr_2(time.time())
    with open(os.path.join(BASE_DIR,"django.log"),"a+") as f:
        f.write("time:%s INFO:%s\n" %(t,msg))

