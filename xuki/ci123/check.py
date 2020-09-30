# @Time : 2020/4/24 17:41
# @Author : Xuki
# @File : check.py
# @Annotation : 上下班打卡

import argparse
import datetime
import random
import time
from ..ifttt import ifttt
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import *

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)
# from ifttt import ifttt

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
EMAIL = 'xumingjing@corp-ci.com'
PASSWORD = 'Xuki123456'
USERID = 165

LOGIN_URL = 'http://oa.corp-ci.com/oa.php/Login/userLogin'
CHECK_URL = 'http://oa.corp-ci.com/oa.php/Punch/newPunch'

CHECK_IN_TYPE = 'one'
CHECK_OUT_TYPE = 'four'


def send_request(_type):
    with requests.session() as session:
        session.headers.update({'User-Agent': USER_AGENT})
        session.post(LOGIN_URL, {'email': EMAIL, 'password': PASSWORD})
        content = session.post(CHECK_URL,
                               {'type': CHECK_IN_TYPE if _type == 'in' else CHECK_OUT_TYPE, 'userId': USERID}).text
        data = content.split('_')[0]
        # data = 'successGift'
        # write_log(content)
        now = datetime.datetime.now()
        if data.startswith('success'):
            ifttt.send('check', {'value2': now.strftime('%H:%M:%S'),
                                 'value1': f'{now.strftime("%m.%d")}上班打卡成功：' if _type == 'in'
                                 else f'{now.strftime("%m.%d")}下班打卡成功：'})
        else:
            ifttt.send('check', {'value2': now.strftime('%H:%M:%S'),
                                 'value1': f'{now.strftime("%m.%d")}上班打卡失败（{data}）：' if _type == 'in'
                                 else f'{now.strftime("%m.%d")}下班打卡失败（{data}）：'})


def write_log(content):
    with open('log/check_log.txt', 'a+', encoding='utf8') as f:
        f.write(content)


def scheduler_listener(ev):
    if ev.exception:
        write_log('job({id}-{time}) is {exception} error'.
                  format(id=ev.job_id, time=ev.scheduled_run_time,
                         exception=ev.exception))
    else:
        write_log('job({id}-{time}) is miss'.format(id=ev.job_id, time=ev.scheduled_run_time))


def check(_type):
    if is_check():
        if _type == 'in':
            check_str = '上班'
            start_datetime = datetime.datetime.today().replace(hour=9, minute=0, second=0, microsecond=0).timestamp()
            end_datetime = datetime.datetime.today().replace(hour=9, minute=10, second=0, microsecond=0).timestamp()
        elif _type == 'out':
            check_str = '下班'
            start_datetime = datetime.datetime.today().replace(hour=19, minute=0, second=0, microsecond=0).timestamp()
            end_datetime = datetime.datetime.today().replace(hour=20, minute=30, second=0, microsecond=0).timestamp()
        else:
            raise ValueError('Type is error')
        run_date = datetime.datetime.fromtimestamp(random.randrange(start_datetime, end_datetime))
        # run_date = datetime.datetime.now() + datetime.timedelta(seconds=3)
        ifttt.send('check', {'value2': run_date.strftime('%H:%M:%S'),
                             'value1': f"{run_date.strftime('%m.%d')}预计{check_str}打卡时间："})
        scheduler = BackgroundScheduler()
        scheduler.add_listener(scheduler_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED)
        scheduler.add_job(send_request, 'date', run_date=run_date, args=(_type,),
                          id=f"{run_date.strftime('%Y-%m-%d_%H:%M:%S')}-{_type}")
        scheduler.start()
        try:
            while len(scheduler.get_jobs()) > 0:
                time.sleep(2)
        except(KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            write_log('Exit the job!')
    else:
        pass


def is_check():
    result = requests.get('http://stock.luckyxuki.cn:9000/is_check', timeout=None).text
    write_log(f"{datetime.datetime.today().strftime('%Y-%m-%d')}打卡检测={result}\n")
    return True if int(result) == 1 else False


