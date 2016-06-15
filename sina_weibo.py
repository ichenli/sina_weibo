#!/usr/bin/env python
# encoding: utf-8

import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
import time
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')

path = './weibo_keyword/'
url_login = 'http://login.weibo.cn/login/'
search_url = 'http://weibo.cn/search/?pos=search&vt=4'

html = requests.get(url_login).content#解析网页
soup = BeautifulSoup(html,'lxml')
selector = etree.HTML(html)

code_img = str(soup.find('img'))[38:-3]#获取验证码图片地址
img = requests.get(code_img).content
output = open('captcha.gif','wb')#保存验证码图片
output.write(img)
output.close()
os.system('eog captcha.gif')#显示验证码
code = raw_input('请输入验证码:')

password = selector.xpath('//input[@type="password"]/@name')[0]#解析所要提交的表单内容
vk = selector.xpath('//input[@name="vk"]/@value')[0]
action = selector.xpath('//form[@method="post"]/@action')[0]
capId = selector.xpath('//input[@name="capId"]/@value')[0]

new_url = url_login + action
data = {'mobile':'yournumber',#构造数据
        password:'yourpassword',
        'code':code,
        'remember':'on',
        'backURL':'http://weibo.cn/search/?tf=5_012&vt=4',
        'backTitle':u'微博',
        'tryCount':'',
        'vk':vk,
        'capId':capId,
        'submit':u'登录'
        }
session = requests.Session()
session.post(new_url,data=data)#提交

p = re.compile(r'\[.+\]')
keyword = ['经济']#关键词暂定一个，大家可以酌情增多
flag = 1#结果命名时的文件名
k = 1#表示程序进度
count = len(keyword)*100
for item in keyword:
    for j in range(1,101):
        page_url = 'http://weibo.cn/search/mblog?hideSearchFrame=&keyword='+item+'&page='+str(j)+'&vt=4'#查询结果链接
        html = session.get(page_url).content
        selector = etree.HTML(html)
        content = selector.xpath('//span[@class="ctt"]')
        if j%50==0 :
            time.sleep(100)
        for each in content :
            text = each.xpath('string(.)')
            #print(text)
            a = p.findall(text)
            if a :
                f = open(path+str(flag)+'.txt','w')#写入结果
                f.write(text)
                f.close()
                flag = flag +1
        k = k+1
        print(str(k)+'/'+str(count))#进度
    break




