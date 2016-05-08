# -*- encoding: UTF-8 -*-

import requests
from pyquery import PyQuery as pq
from selenium import webdriver
from ConfigParser import ConfigParser
import datetime
import time
import stockPre
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class XueqiuScrapy:

    def __init__(self):

        conf = ConfigParser()
        conf.read('conf.ini')
        self.log_url = 'https://xueqiu.com/user/login'
        self.log_data = dict(conf.items('account'))
        self.header = dict(conf.items('header'))
    # get page from Xueqiu with webdriver
    def getPagePan(self):

        # driver = webdriver.PhantomJS()
        driver = webdriver.Chrome()

        testurl = 'http://xueqiu.com/hq'
        driver.get(testurl)

        time.sleep(3)

        return driver.page_source.decode('utf-8')

    def getInfoTop(self,html):

        doc = pq(html)
        list = []
        for i in range(3,6):
            leaf = doc('div.stock-rank').eq(i)
            eachtop=[]
            for k in range(1,11):
                eachtop.append(leaf('tr').eq(k).find('td').eq(0).text())

            list.append(eachtop)

        return list



    def getPage(self):
        session = requests.session()

        res = session.post(url=self.log_url,data=self.log_data,headers=self.header)

        m_cookie = res.cookies
        cookie_dic = dict(m_cookie.items())
        for item in cookie_dic.keys():
            print item

        print 'writing file ... done'
        testurl = 'https://xueqiu.com/hq/screener'
        res = session.get(url=testurl,headers = self.header,cookies = m_cookie)
        return res.text.decode('utf-8')


Xueqiu = XueqiuScrapy()

page = Xueqiu.getPagePan()
#print Xueqiu.getPage()
# with open('xueqiuini.html', 'w') as f:
#     f.write(page)



datetoday = datetime.datetime.now()

todaystr=datetoday.strftime('%Y-%m-%d')

if os.path.exists(todaystr):
    print todaystr+' has been exist'
else:
    os.mkdir(todaystr)

for i in range(3):
    with open(todaystr+'/'+str(i),'w') as f:
        for item in Xueqiu.getInfoTop(page)[i]:
            print item
            f.write(item+'\n')



#对昨天的存储数据进行股票模拟
stockPrice = stockPre.stockPre()



