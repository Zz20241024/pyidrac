#coding=utf-8
import json
from collections import defaultdict
from .pconf import PTYPES,purls
import re
import pprint

def common_handle(info,fields):
    r_data = defaultdict(dict)
    info = json.loads(info)
    type, data = list(info.items())[0]
    for i in data.values():
        pinfo = {}
        name = i.get(fields[0], 'none')
        for ii in fields[1:]:
            pinfo.setdefault(ii, i.get(ii, ''))
        r_data[type][name] = pinfo
    r_data[type].pop("none") if "none" in r_data[type] else 0
    return r_data

def pother(info,fields):
    r_data = dict()
    for i in fields:
        re_string="<{}>(.+?)</{}>".format(i,i)
        data=re.search(re_string,info)
        if data:r_data[i]=data.group(1)
    return {"psys":r_data}

def psysinfo(info,fields):
    r_data = dict()
    info = json.loads(info)
    if type(info) == dict:
        for i in fields:
            r_data[i]=info.get(i,"")
    return {"psys":r_data}
def pidrac(info,fields):
    r_data = dict()
    info = json.loads(info)
    if type(info) == dict:
        for i in fields:
            r_data[i]=list(info.values())[0].get(i,"")
    return {"idrac":r_data}
#main
def parse(data):
    r_data={}
    ip, pdata = list(data.items())[0]
    for type, info in pdata.items():

        if info and info.find("</html>") <0:
            if type == "pother":
                r_data.update(pother(info,purls[type][1]))
            elif type in ["psysinfo"]:
                r_data.update(psysinfo(info,purls[type][1]))
            elif type in ["pidrac"]:
                r_data.update(pidrac(info, purls[type][1]))

            else:
                r_data.update(common_handle(info, purls[type][1]))
        else:
            r_data.update({type:info})

    return {ip:r_data}
#test

