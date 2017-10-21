#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
Info
- author : "xchaoinfo"
- email  : "xchaoinfo@qq.com"
- date   : "2016.4.8"

3.4 遇到一些问题，于 4.8 号解决。
这里遇到的问题是 跨域请求时候， headers 中的 Host 不断变化的问题，需要针对
不同的访问，选择合适的 Host
3.4 遇到问题，大概是忽略了更换 Host 的问题
'''
import requests
import re
import json
import base64
import time
import math
import random
from PIL import Image
from selenium import webdriver
import time
try:
    from urllib.parse import quote_plus, urlencode
    from urllib.request import Request, urlopen
except:
    from urllib import quote_plus

'''
3.4
所有的请求都分析的好了
模拟请求 一直不成功
在考虑是哪里出了问题
以后学了新的知识后 再来更新
'''

# 构造 Request headers
agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
global headers
headers = {
    "Host": "passport.weibo.cn",
    "Connection": "keep-alive",
    #"Upgrade-Insecure-Requests": "1",
    'User-Agent': agent,
    #'Cookie':'SCF=AmIUKtHS7AIywbvtgBJBtoPWwj3wOcv2G3207YGIeF0NNue0tt_Ge6vWVjUEd3QUDn4c-DqYsps_dA7HCweULLE.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhJ_IPIhF_kXjOlLbL26L955JpX5KMhUgL.FoeESo.Eeh.0SKe2dJLoI7L0UJSyMN9yUc-t; _T_WM=49cf8f06c1cc3a3efdeae7b2c62ff130; H5:PWA:UID=1; SUHB=0k1CEVE6JbDi9V; H5_INDEX=3; H5_INDEX_TITLE=svcasvawe; SUB=_2AkMutXoxdcPxrABTnvEXzGLhaY5H-jydYBPHAn7oJhMyPRh77l8DqSekNH8YzeYyUNrTyRfiFLNAT9_Plg..; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D10000011%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home%26fid%3D102803_ctg1_8999_-_ctg1_8999_home%26uicode%3D10000011'
}

session = requests.session()
# 访问登录的初始页面
index_url = "https://passport.weibo.cn/signin/login"
session.get(index_url, headers=headers)


def get_su(username):
    """
    对 email 地址和手机号码 先 javascript 中 encodeURIComponent
    对应 Python 3 中的是 urllib.parse.quote_plus
    然后在 base64 加密后decode
    """
    username_quote = quote_plus(username)
    username_base64 = base64.b64encode(username_quote.encode("utf-8"))
    return username_base64.decode("utf-8")


def login_pre(username):
    # 采用构造参数的方式
    params = {
        "checkpin": "1",
        "entry": "mweibo",
        "su": get_su(username),
        "callback": "jsonpcallback" + str(int(time.time() * 1000) + math.floor(random.random() * 100000))
    }
    '''真是日了狗，下面的这个写成 session.get(login_pre_url，headers=headers) 404 错误
        这条 3.4 号的注释信息，一定是忽略了 host 的变化，真是逗比。
    '''
    pre_url = "https://login.sina.com.cn/sso/prelogin.php"
    headers["Host"] = "login.sina.com.cn"
    headers["Referer"] = index_url
    pre = session.get(pre_url, params=params, headers=headers)
    #print('pre:'+pre.text)
    pa = r'\((.*?)\)'
    res = re.findall(pa, pre.text)
    #print(res)
    if res == []:
        print("好像哪里不对了哦，请检查下你的网络，或者你的账号输入是否正常")
    else:
        js = json.loads(res[0])
        #print(js)
        if js["showpin"] == 1:
            headers["Host"] = "passport.weibo.cn"
            capt = session.get("https://passport.weibo.cn/captcha/image", headers=headers)
            capt_json = capt.json()
            capt_base64 = capt_json['data']['image'].split("base64,")[1]
            with open('capt.jpg', 'wb') as f:
                f.write(base64.b64decode(capt_base64))
                f.close()
            im = Image.open("capt.jpg")
            im.show()
            im.close()
            cha_code = input("请输入验证码\n>")
            return cha_code, capt_json['data']['pcid']
        else:
            return ""


def login(username, password):
    postdata = {
        "username": username,
        "password": password,
        "savestate": "1",
        "ec": "0",
        "pagerefer": "https://m.weibo.cn/p/102803_ctg1_8999_-_ctg1_8999_home",
        "entry": "mweibo",
        "wentry": "",
        "loginfrom": "",
        "client_id": "",
        "code": "",
        "qq": "",
        "mainpageflag":"1",
        "hff": "",
        "hfp": ""
    }
    ''''
    if pincode == "":
        pass
    else:
        postdata["pincode"] = pincode[0]
        postdata["pcid"] = pincode[1]
    '''
    headers["Host"] = "passport.weibo.cn"
    headers["Reference"] = index_url+"?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn"
    headers["Origin"] = "https://passport.weibo.cn"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    post_url = "https://passport.weibo.cn/sso/login"
    postdata = urlencode(postdata).encode('utf-8')
    login = session.post(post_url, data=postdata, headers=headers)
    #print(login.cookies)
    #print(login.status_code)
    js = login.json()
    #print(js)
    uid = js["data"]["uid"]

    #crossdomain = js["data"]["crossdomainlist"]
    cn = js['data']['loginresulturl']
    #print(cn)
    # 下面两个对应不同的登录 weibo.com 还是 m.weibo.cn
    # 一定要注意更改 Host
    # mcn = "https:" + crossdomain["weibo.cn"]
    # com = "https:" + crossdomain['weibo.com']
    headers["Host"] = "login.sina.com.cn"
    session.get(cn, headers=headers)

    headers["Host"] = "m.weibo.cn"
    ht = session.get("http://m.weibo.cn/u/%s" % uid, headers=headers)
    #print(ht.text)
    pa = r'<title>(.*?)</title>'
    res = re.findall(pa, ht.text)
    #print(res)
    print("你好%s，你正在使用 xchaoinfo 写的模拟登录" % res[0])
    # print(cn, com, mcn)

    driver = webdriver.PhantomJS(executable_path='/home/wyq/application/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.get("http://m.weibo.cn/u/%s" % uid)
    time.sleep(10)
    print(driver.find_elements_by_tag_name('span'))


if __name__ == "__main__":

    username = input('用户名：')
    password = input('密码：')
    pincode = login_pre(username)
    login(username, password)
