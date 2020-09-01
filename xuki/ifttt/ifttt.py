# @Time : 2020/8/28 16:25
# @Author : Xuki
# @File : ifttt.py
# @Annotation :使用ifttt发送push

import requests


def send(event_name, values):
    key = 'd52n-XLnjmsFF9fZ6AX6sB'
    url = f'https://maker.ifttt.com/trigger/{event_name}/with/key/{key}'
    ret = requests.post(url, json=values).text


if __name__ == '__main__':
    send('stock', {'value1': '2020-08-28 19:32:21'})
    send('check', {'value1': '2020-08-28 19:32:21', 'value2': ' 打下班卡成功'})
