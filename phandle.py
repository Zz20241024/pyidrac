#coding=utf-8
from .precvinfo import rec_data
from .pparse import parse
from threading import Thread,RLock
import pprint,time
from  .pconf import PTHREAD_NUM
import sys,re
import traceback
from multiprocessing import Process
from threading import Thread,Event
from queue import Empty, Full,Queue
from .putil import logger

#放进queue队列
def put_queue_data(ip,pqueue,U_P):
    data = rec_data(ip,*U_P)

    if data:
        pqueue.put(parse(data),timeout=10)
    else:
        raise Exception("dont pick up headers")

def put_queue_thread(qlock,ips,pqueue,U_P):
    while 1:
        with qlock:
            if len(ips) == 0:return
            ip=ips.pop()
        try:
            put_queue_data(ip,pqueue,U_P)
        except Exception as e:
            logger("ip:{};error:{}".format(ip, e))
            #print("ip:{};error:{}".format(ip,traceback.format_exc()))
def get_process(*arg):
    return [Process(target=arg[0], args=arg[1:-1]) for i in range(arg[-1])]

def get_threads(*arg):
    return [Thread(target=arg[0], args=arg[1:-1]) for i in range(arg[-1])]

def _produce_info(ips,pqueue,pevent,U_P,num=PTHREAD_NUM):
    logger("method:{} begin to work".format(_produce_info.__name__).center(40,"*"))
    qlock = RLock()
    parse_data_threads=get_threads(put_queue_thread,qlock,ips,pqueue,U_P,num)
    for i in parse_data_threads:
        i.start()
    for i in parse_data_threads:
        i.join()
    pevent.set()
    logger("method:{} work is over".format(_produce_info.__name__).center(40,"*"))
    sys.exit(0)


class Host(object):
    def __len__(self):
        return self.q.qsize()
    def __init__(self,q=None,e=None):
        self.q=q
        self.e=e
    def __iter__(self):
        return self

    def done(self):
        return True if (self.e.is_set() and self.q.empty()) else False

    def __next__(self):
        if self.done():
            raise StopIteration
        try:
            data=self.q.get(timeout=3)
        except Empty as e:
            data=''
        return data


    def fetchone(self):
        return next(self)

    def fetchall(self):
        datas=[]
        for i in self:
            datas.append(i)
        return datas



def get_hosts_info(ips,user=None,password=None):
    pqueue = Queue()
    pevent=Event()
    U_P=(user,password)
    if type(ips) is not list:
        ips=[ips]
    Thread(target=_produce_info,args=(ips,pqueue,pevent,U_P)).start()
    return Host(pqueue,pevent)








