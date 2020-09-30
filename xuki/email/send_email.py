# @Time : 2020/9/30 11:40
# @Author : Xuki
# @File : send_email.py
# @Annotation : 

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

msg_from = '574325507@qq.com'  # 发送方邮箱
passwd = 'eqgoxouriurmbdib'  # 填入发送方邮箱的授权码

s = smtplib.SMTP_SSL("smtp.qq.com", 465)
s.login(msg_from, passwd)


def send(tos, subject, content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = formataddr(["Father", msg_from])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    for to in tos:
        msg['To'] = formataddr(["Son", to])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        try:
            s.sendmail(msg_from, to, msg.as_string())
        except smtplib.SMTPException:
            pass
        finally:
            s.quit()
