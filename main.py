from email.header import Header
from email.mime.text import MIMEText

from Ashare import *
import smtplib
import os


def send_email(body):
    smtp_mail = os.environ.get('SMTP_MAIL')
    smtp_token = os.environ.get('SMTP_TOKEN')

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
        if body != '':
            # 发送邮件
            server.sendmail(sender, recipient, msg.as_string())
            print("邮件已发送")
        else:
            print("无需发送邮件")
    else:
        print("SMTP 登录失败")

    # 关闭连接
    server.quit()


if __name__ == '__main__':
    dfTenYears = get_price('sh000001', frequency='1d', count=2426)

    lowLine = dfTenYears['close'].mean()
    highLine = lowLine + 450

    dfOneDay = get_price('sh000001', frequency='1d', count=1)

    lowPoint = dfOneDay['low'].mean()
    highPoint = dfOneDay['high'].mean()

    body = f"当前高水位是：{highLine}\n" \
           f"当前收盘价是：{dfOneDay['close'].mean()}\n" \
           f"当前低水位是：{lowLine}"

    print(body)

    if lowPoint < lowLine:
        send_email(f"当前最低点是：{lowPoint}\n"
                   f"当前低水位是：{lowLine}\n"
                   f"该买了")
    elif highPoint > highLine:
        send_email(f"当前最高点是：{highPoint}\n"
                   f"当前高水位是：{highLine}\n"
                   f"该卖了")
    else:
        send_email('')
