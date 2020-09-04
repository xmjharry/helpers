# @Time : 2020/8/28 17:54
# @Author : Xuki
# @File : shoot.py
# @Annotation :

import argparse
from xuki.ci123.check import check
from xuki.wannianli import rili
from xuki import config
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('action', help='具体的操作')
parser.add_argument('--type', help='in代表上班打卡，out代表下班打卡')
parser.add_argument('--date', default=datetime.datetime.today().strftime('%Y-%m-%d'), help='获取当前日期是假期还是工作日')
args = parser.parse_args()
_action = args.action

if _action == 'check' and config.CHECK:
    check(args.type)


if _action == 'holiday':
    rili.judge(args.date)
