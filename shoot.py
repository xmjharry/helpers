# @Time : 2020/8/28 17:54
# @Author : Xuki
# @File : shoot.py
# @Annotation :

import argparse
from xuki.ci123.check import check
from xuki import config

parser = argparse.ArgumentParser()
parser.add_argument('action', help='具体的操作')
parser.add_argument('--type', help='in代表上班打卡，out代表下班打卡')
args = parser.parse_args()
_action = args.action

if _action == 'check' and config.CHECK:
    check(args.type)
