# @Time : 2021/2/24 19:30
# @Author : Xuki
# @File : create_channel.py
# @Annotation : 

import pandas as pd
import json
import requests
import time
import random
import itertools


def get_key(_dict, _value):
    for key, value in _dict.items():
        if _value == value:
            return str.upper(key)
    return 'NUL'


def insert_channel_way(code):
    ret = requests.post('http://180.96.7.122:10090/api/contact/addPregnoticeChannel', {'code': code}).text
    ret = json.loads(ret)
    if ret.get('status') != 'success':
        print(f'addPregnoticeChannel出错,{code}')
        return 0
    ret = requests.post('http://180.96.7.122:10090/api/contact/way/create', {'state': code}).text
    ret = json.loads(ret)
    if ret.get('status') != 'success':
        print(f'way/create出错，{code}')
        return 0
    time.sleep(random.randint(1, 2))
    print(f'code={code}执行成功')
    return 1


for code in itertools.product(['STX', 'ETX', 'AA', 'AB', 'AC', 'AD', 'BA'], ['NUL'], ['NUL']):
    code = '-'.join(code)
    ret = insert_channel_way(code)
    if ret == 0:
        break
exit(0)


config = json.load(open('config.json'))
city = config['city']
province = config['province']

data = pd.read_excel('channel.xlsx')
data['状态标签'] = data['状态标签'].ffill()

for index, row in data.iterrows():
    code = (row['状态标签'] + '-' + get_key(city, row['城市标签'])
            + '-' + get_key(province, row['省份标签']))
    data.loc[index, '邀请码'] = data.loc[index, '渠道码'] = code
    ret = insert_channel_way(code)
    if ret == 0:
        break

print('success')
writer = pd.ExcelWriter('channel_perfect.xlsx')
data.to_excel(writer)
writer.save()
