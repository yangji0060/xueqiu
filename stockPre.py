# -*- encoding:UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import tushare as ts
import datetime


class stockPre():
#从abc.csv建立字典,映射股票中文名和代码
    def __init__(self):
        self.dictSto = {}

        with open('abc.csv', 'r') as f:
            f.readline()
            line = f.readline()
            while line:
                linelist = line.strip().split(',')
                linelist[2] = linelist[2].replace(' ', '')
                self.dictSto.setdefault(linelist[2])
                self.dictSto[linelist[2]] = linelist[1]
                # print linelist
                line = f.readline()
        self.code = ''

    def getCode(self):

        return self.code

    def setCodefromname(self,name):

        if self.dictSto.has_key(name):

            self.code = self.dictSto[name]
            return True

        else:
            return False



#获得当天的股票价格信息
    def getNowSto(self):

        dict = {}

        nowtime = datetime.datetime.now()
        nowtimestr = nowtime.strftime('%Y-%m-%d')

        stoRealtime = ts.get_hist_data(self.code, start=nowtimestr, end=nowtimestr)

        if(len(stoRealtime) != 0):

            dict['open'] = stoRealtime.iloc[0,0]
            dict['high'] = stoRealtime.iloc[0,1]
            dict['low'] = stoRealtime.iloc[0,2]
            dict['close'] = stoRealtime.iloc[0,3]

        return dict

    #获得上一个交易日的股票价格信息
    def getLasSto(self):

        nowtime = datetime.datetime.now()

        nowweek = nowtime.weekday()
        if nowweek == 6 or nowweek == 0:
            a = -3
        elif nowweek == 5:
            a = -2
        else:
            a = -1

        yestime = nowtime + datetime.timedelta(days=a)

        yestimestr = yestime.strftime('%Y-%m-%d')

        tsyes = ts.get_hist_data(self.code, start=yestimestr, end=yestimestr)

        dict = {}
        if(len(tsyes) != 0):
            dict['open'] = tsyes.iloc[0,0]
            dict['high'] = tsyes.iloc[0,1]
            dict['close'] = tsyes.iloc[0,2]
            dict['low'] = tsyes.iloc[0,3]

        return dict


if __name__ == '__main__':

    name = '多氟多'

    abc = stockPre()
    code = abc.getCode()
    print code
    print abc.setCodefromname(name)

    nowsto = abc.getNowSto()
    lassto = abc.getLasSto()

    print 'today\'s stock is ',nowsto
    print 'yestoday\'s stock is ',lassto