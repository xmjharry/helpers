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
        session.post(CHECK_URL, {'type': CHECK_IN_TYPE if _type == 'in' else CHECK_OUT_TYPE, 'userId': USERID})
    ifttt.send('check', {'value2': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                         'value1': '今天上班打卡时间：' if _type == 'in' else '今天下班打卡时间：'})
    with open('log/check_log.txt', 'a+', encoding='utf8') as f:
        f.write(
            datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '上班打卡成功\n' if _type == 'in' else '下班打卡成功\n')


def check(_type):
    if _type == 'in':
        strat_datetime = datetime.datetime.today().replace(hour=8, minute=50, second=0, microsecond=0).timestamp()
        end_datetime = datetime.datetime.today().replace(hour=9, minute=15, second=0, microsecond=0).timestamp()
    elif _type == 'out':
        strat_datetime = datetime.datetime.today().replace(hour=19, minute=0, second=0, microsecond=0).timestamp()
        end_datetime = datetime.datetime.today().replace(hour=20, minute=30, second=0, microsecond=0).timestamp()
    else:
        raise ValueError('Type is error')
    run_date = datetime.datetime.fromtimestamp(random.randrange(strat_datetime, end_datetime))
    # run_date = datetime.datetime.now() + datetime.timedelta(seconds=1)
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_request, 'date', run_date=run_date, args=(_type,),
                      id=f"{run_date.strftime('%Y-%m-%d %H:%M:%S')}-{_type}")
    scheduler.start()
    try:
        while len(scheduler.get_jobs()) > 0:
            time.sleep(2)
    except(KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit the job!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('type', help='in代表上班打卡，out代表下班打卡')
    args = parser.parse_args()
    _type = args.type
    check(_type)
