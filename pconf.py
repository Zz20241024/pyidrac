#coding=utf-8
import re
#密码
USER_PASS_URLS=[
        ("root","","/data/login"),
        ("root","","/sysmgmt/2015/bmc/session"),
    ("root","","/data/login"),
    ("root","","/sysmgmt/2015/bmc/session"),




]

#线程
PTHREAD_NUM=50
TIME_OUT=10
#配置urls
root_url="https://{}"
purls=dict(pprocessor=("/sysmgmt/2012/server/processor",["device_description","brand","version","core_count","status","current_speed"]),
pcontrol=("/sysmgmt/2010/storage/controller",["enclosures","name","driver_version","firmware_version","cache_size","rollup_status","status"]),
pmemory=("/sysmgmt/2012/server/memory",["name","type","size","speed","status",]),
pdisk=("/sysmgmt/2010/storage/pdisk",["name","size","slot","status","remaining_drive_life","firmware_version","media_type","protocol"]),
#pdetail="/data?get=pwState,sysDesc,sysRev,svcTag,iDSDMVersion,v4Enabled,v4IPAddr,v6Enabled,v6LinkLocal,v6Addr,v6SiteLocal,macAddr,dnsDomain,devLocInfo,osVersion,kvmEnabled,lcdChassisStatus,hostEventStatus,lcdEventStatus",
psysinfo=("/sysmgmt/2015/server/sysinfo",["OSName","OSVersion","SystemModelName","SystemServiceTag","HostName","MACAddress"]),
pidrac=("/sysmgmt/2012/server/configgroup/iDRAC.NIC",["MACAddress"]),
pother=("/data?get=sysDesc,svcTag,hostName,osName,macAddr",["sysDesc","svcTag","hostName","osName","macAddr","osVersion"]),

)
PTYPES=list(purls.keys())
#settings
class URLSettings(object):
    def __init__(self,ip):
        self.ip=ip
        self.root_url=root_url.format(self.ip)

    def __getitem__(self, item):
        if item == "plogin":
            return [(i[0],i[1],self.root_url+i[2]) for i in USER_PASS_URLS]
        return self.root_url+purls[item][0]

