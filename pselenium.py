from  selenium import webdriver
import os,sys
from selenium.webdriver.common.keys import Keys
import re
import time
import traceback
from .putil import logger
ST2='''var TOKEN_VALUE = "(.+)";'''
user_id="user"
password_id="password"
login_id="btnOK"
drive_path=os.path.dirname(__file__)
chrome_driver_path=os.path.join(drive_path,"chromedriver")
phantomjs_driver_path=os.path.join(drive_path,"phantomjs")
foxfire_driver_path=os.path.join(drive_path,"geckodriver")
def rec_token(url,userpassword):
    url=re.search(r"https://.+?/",url).group(0)+"login.html"
    page,cookies=page_source(url,userpassword)
    r_token=re.search(ST2,page).group(1)
    cookie=cookies["name"]+"="+cookies["value"]
    header={
                "Cookie": cookie,
                'ST2': r_token,
                "X_SYSMGMT_OPTIMIZE": "true",
                "X-SYSMGMT-OPTIMIZE": "true",
                "user": userpassword["user"],
                "password": userpassword["password"],

            }
    #print(header)
    return header
def token(url,userpassword):

    try:
        header=rec_token(url,userpassword)
    except Exception as e:
        logger("seleniumurl:%s;error:s%" % (url,e))
        header = {}
    return header






def page_source(url,userpassword):
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('-headless')
    #chrome_options.add_argument('--disable-gpu')
    #driver=webdriver.Chrome(executable_path=chrome_driver_path,chrome_options=chrome_options)
    driver=webdriver.Firefox(executable_path=foxfire_driver_path,firefox_options=firefox_options)
    driver.get(url)
    time.sleep(5)
    driver.find_element_by_id(user_id).send_keys(userpassword["user"])
    driver.find_element_by_id(password_id).send_keys(userpassword["password"])
    driver.find_element_by_id(login_id).send_keys(Keys.RETURN)
    time.sleep(8)
    page=driver.page_source
    cookies=driver.get_cookie("_appwebSessionId_")
    #print(page,cookies)
    driver.close()
    return page,cookies




