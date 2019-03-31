# pyidrac
idrac服务器详细信息获取

# 使用范围
适用于dell服务器,其他服务器资产信息待测定.我会不断的更新bug.

# python版本
python2，python3

# 使用说明
## 安装
pip install pyidrac
## 使用
from pyidrac import get_hosts_info \n
z=get_hosts_info(['ip1','ip2'],"user","password") \n
## 获取结果:
z.fetchone 单个结果\n
z.fetchall()所有结果\n



