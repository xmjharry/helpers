# @Time : 2020/4/24 17:41
# @Author : Xuki
# @File : check_in.py
# @Annotation : 

import requests
import time
import random
import argparse

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
EMAIL = 'xumingjing@corp-ci.com'
PASSWORD = 'Xuki123456'
USERID = 165

LOGIN_URL = 'http://oa.corp-ci.com/oa.php/Login/userLogin'
CHECK_URL = 'http://oa.corp-ci.com/oa.php/Punch/newPunch'

CHECK_IN_TYPE = 'one'
CHECK_OUT_TYPE = 'four'

minute = random.randint(0, 13)
second = random.randint(0, 60)
time.sleep(minute * 60 + second)

parser = argparse.ArgumentParser()
parser.add_argument('--type', help='in代表上班打卡，out代表下班打卡', default='in')
args = parser.parse_args()
_type = args.type
with requests.session() as session:
    session.headers.update({'User-Agent': USER_AGENT})
    session.post(LOGIN_URL, {'email': EMAIL, 'password': PASSWORD})
    session.post(CHECK_URL, {'type': CHECK_IN_TYPE if _type == 'in' else CHECK_OUT_TYPE, 'userId': USERID})
