# @Time : 2020/4/24 17:41
# @Author : Xuki
# @File : check.py
# @Annotation : 

import argparse
import datetime
import random
import time
import requests
from apscheduler.schedulers.background import BackgroundScheduler

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
EMAIL = 'xumingjing@corp-ci.com'
PASSWORD = 'Xuki123456'
USERID = 165

LOGIN_URL = 'http://oa.corp-ci.com/oa.php/Login/userLogin'
CHECK_URL = 'http://oa.corp-ci.com/oa.php/Punch/newPunch'

CHECK_IN_TYPE = 'one'
CHECK_OUT_TYPE = 'four'


def check():
    with requests.session() as session:
        session.headers.update({'User-Agent': USER_AGENT})
        session.post(LOGIN_URL, {'email': EMAIL, 'password': PASSWORD})
        session.post(CHECK_URL, {'type': CHECK_IN_TYPE if _type == 'in' else CHECK_OUT_TYPE, 'userId': USERID})


parser = argparse.ArgumentParser()
parser.add_argument('type', help='in代表上班打卡，out代表下班打卡')
args = parser.parse_args()
_type = args.type

strat_datetime = None
end_datetime = None

if _type == 'in':
    strat_datetime = datetime.datetime.today().replace(hour=8, minute=50, second=0, microsecond=0).timestamp()
    end_datetime = datetime.datetime.today().replace(hour=9, minute=15, second=0, microsecond=0).timestamp()
elif _type == 'out':
    strat_datetime = datetime.datetime.today().replace(hour=19, minute=0, second=0, microsecond=0).timestamp()
    end_datetime = datetime.datetime.today().replace(hour=20, minute=30, second=0, microsecond=0).timestamp()
else:
    raise ValueError('Type is error')
run_date = datetime.datetime.fromtimestamp(random.randrange(strat_datetime, end_datetime))
scheduler = BackgroundScheduler()
scheduler.add_job(check, 'date', run_date=run_date, args=(), id=f"{run_date.strftime('%Y-%m-%d %H:%M:%S')}-{_type}")
scheduler.start()
try:
    while len(scheduler.get_jobs()) > 0:
        time.sleep(2)
except(KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print('Exit the job!')
