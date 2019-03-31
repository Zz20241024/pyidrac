#coding=utf-8
import json
import sys,time,re,os
from .pconf import URLSettings,purls,PTYPES,TIME_OUT
import requests,pprint
from .pselenium import token
ST2=re.compile(r'ST2=(.+?)\b')
ST1=re.compile(r'ST1=(.+?)\b')
from .putil import logger
#登录获取header
def r_get_post(url,method="GET",**kwargs):
    resp=''
    if method.lower()=="get":
        with requests.get(url,**kwargs) as resp:
            return resp
    if method.lower() == "post":
        with requests.post(url,**kwargs) as resp:
            return resp
    return resp


def try_request(url,ip,method,**kwargs):
    resp=''
    try:
        resp=r_get_post(url,method=method,**kwargs)
    except Exception as e:
        logger("host:{};url:{};method:{},error:{}".format(ip,url,method,e))
    return resp

def multi_try_request(url,ip,method,**kwargs):
    resp=''
    def request(t=0):
        time.sleep(t)
        return try_request(url,ip,method=method,**kwargs)
    resp =request(0)
    return resp

#登录
def get_header(resp,data,url):
    #print(resp.text, data,url, resp.headers,list(resp.cookies),dir(resp),resp.url)
    st2 = ST2.search(resp.content.decode())
    st1 = ST1.search(resp.content.decode())
    XSRF_TOKEN = resp.headers.get("XSRF-TOKEN", '')
    if st1 or st2 or XSRF_TOKEN:
        cookie = resp.headers["Set-Cookie"]
        cookie = cookie.split(";")[0]
        if st1 and not st2:
            return token(url, data)

        else:
            return {
                "Cookie": cookie,
                'ST2': st2.group(1) if st2 else "",
                "X_SYSMGMT_OPTIMIZE": "true",
                "X-SYSMGMT-OPTIMIZE": "true",
                "XSRF-TOKEN": XSRF_TOKEN,
                "user": data["user"],
                "password": data["password"],

            }


def rec_header(up_urls,ip,*userpass):
    headers={}
    if userpass and len(userpass) ==2:
        up_urls=[(userpass[0],userpass[1],up_url[2]) for up_url in up_urls]
    def r_headers(up_url,ip=ip):
        data={"user":up_url[0],"password":up_url[1]}
        resp=multi_try_request(up_url[2],ip,method="POST",data=data,headers=data,verify=False,timeout=TIME_OUT)
        if resp:return get_header(resp,data,up_url[2])
    for i in up_urls:
        headers=r_headers(i)
        if headers:
            break
    return headers



#采集区
def rec_handle(url,ip,headers,method="GET"):
    resp=multi_try_request(url, ip,headers=headers, verify=False,timeout=TIME_OUT,method=method)
    return resp

def rec_info(info_types,headers,urlsettings):
    data={}
    for type in info_types:
        method = "GET"
        r_data=rec_handle(urlsettings[type],urlsettings.ip, headers=headers,method=method)
        data[type] = r_data.text if r_data else ''
    return data

def rec_data(ip,*userpass):
    urlsettings=URLSettings(ip)
    headers=rec_header(urlsettings["plogin"],ip,userpass)
    if headers:
        data = rec_info(PTYPES, headers, urlsettings)
        #print(headers,ip)
        return {
                ip: data
            }

    return ''




















