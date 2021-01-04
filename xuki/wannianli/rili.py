# @Time : 2020/9/3 18:31
# @Author : Xuki
# @File : rili.py
# @Annotation :
import csv
import datetime
import os

import pandas as pd
import requests
from lxml import etree

file_name = None


class WanNianRiLi(object):
    """万年日历接口数据抓取
    Params:year 四位数年份字符串
    """

    def __init__(self, year):
        self.year = year
        data = self.parseHTML()
        if data:
            self.exportCSV(data)

    def parseHTML(self):
        result = []
        # 生成月份列表
        dateList = [self.year + '-' + '%02d' % i for i in range(1, 13)]
        for year_month in dateList:
            url = 'https://wannianrili.51240.com/ajax/'
            payload = {'q': year_month}
            response = requests.get(url, params=payload)
            element = etree.HTML(response.text)
            html = element.xpath('//div[@class="wnrl_riqi"]')
            # print('In Working:', year_month)
            for _element in html:
                # 获取节点属性
                item = _element.xpath('./a')[0].attrib
                if 'class' in item:
                    if item['class'] == 'wnrl_riqi_xiu':
                        tag = '休假'
                    elif item['class'] == 'wnrl_riqi_ban':
                        tag = '补班'
                    else:
                        pass
                    _span = _element.xpath('.//text()')
                    result.append({'Date': year_month + '-' + _span[0], 'Holiday': _span[1], 'Tag': tag})
        # print(result)
        return result

    def exportCSV(self, data):
        """导出CSV"""
        headers = ['Date', 'Holiday', 'Tag']
        # 如果存入乱码，添加 encoding='utf-8-sig'
        with open(file_name, 'w', newline='', encoding='utf8') as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writeheader()
            f_csv.writerows(data)


# 1-工作日 0-休息日
def judge(date) -> int:
    date_ = datetime.datetime.strptime(date, '%Y-%m-%d')
    year = date_.year
    global file_name
    file_name = f'./xuki/wannianli/{year}Holiday.csv'
    if not os.path.exists(file_name):
        WanNianRiLi(str(year))
    if os.path.exists(file_name):
        result = pd.read_csv(file_name)
        ret = result[result['Date'] == date]
        if len(ret):
            tag = ret.Tag.values[0]
            if tag == '休假':
                return 0
            elif tag == '补班':
                return 1
            else:
                return 1
    day_in_week = date_.isoweekday()
    if day_in_week <= 5:
        return 1
    else:
        return 0


if __name__ == '__main__':
    ret = judge('2021-01-09')
    print(ret)
