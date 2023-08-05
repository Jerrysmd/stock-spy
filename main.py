import os
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText

from Ashare import *


def send_email(body):
    smtp_mail = os.environ.get('SMTP_MAIL')
    smtp_token = os.environ.get('SMTP_TOKEN')
    LAST_EMAIL_TIMESTAMP = os.environ.get('LAST_EMAIL_TIMESTAMP', "0")

    print(f"LAST_EMAIL_TIMESTAMP: {LAST_EMAIL_TIMESTAMP}")

    # 设置发件人和收件人的邮箱地址
    sender = smtp_mail
    recipient = smtp_mail

    # 设置邮件主题
    subject = "Github Actions: stock-spy Repository Remind"

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["from"] = sender
    msg["to"] = recipient

    # 连接到SMTP服务器
    server = smtplib.SMTP("smtp.qq.com")

    # 登录到SMTP服务器
    status, response = server.login(smtp_mail, smtp_token)

    if status == 235:
        print("SMTP 登录成功")
        if body != '' and (time.time() - float(LAST_EMAIL_TIMESTAMP) > 3600 * 24 * 30):
            # 发送邮件
            server.sendmail(sender, recipient, msg.as_string())
            print("邮件已发送")
            os.environ['LAST_EMAIL_TIMESTAMP'] = str(time.time())
        else:
            print("无需发送邮件")
    else:
        print("SMTP 登录失败")

    # 关闭连接
    server.quit()


if __name__ == '__main__':
    kLine_2500day = get_price('sh000001', frequency='1d', count=2500)
    kLine_200day = get_price('sh000001', frequency='1d', count=170)
    kLine_day = get_price('sh000001', frequency='1d', count=1)

    low_water = kLine_2500day['close'].mean()
    high_water = low_water + 450
    day200_water = kLine_200day['close'].mean()

    low_of_day = kLine_day['low'].mean()
    high_of_day = kLine_day['high'].mean()

    msg_body = f"当前高水位是：{high_water}\n" \
               f"当前收盘价是：{kLine_day['close'].mean()}\n" \
               f"当前低水位是：{low_water}"

    print(msg_body)

    if low_of_day < low_water:
        send_email(f"当日最低点是：{low_of_day}\n"
                   f"当前低水位是：{low_water}\n"
                   f"该考虑买了")
    elif high_of_day > high_water or day200_water > high_water:
        send_email(f"当日最高点是：{high_of_day}\n"
                   f"当前高水位是：{high_water}\n"
                   f"该考虑卖了")
    else:
        send_email('')
