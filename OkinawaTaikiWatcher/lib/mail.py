#!python3
# -*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_smtp(host, port, login_mail, login_pw, subject, fr, to, msg):
    # smtp
    mail = smtplib.SMTP(host, port)
    mail.ehlo()
    mail.starttls()

    mail.login(login_mail, login_pw)

    info = MIMEText("閾値を超えた物質があります。" + os.linesep + msg, 'plain', 'utf-8')
    info['Subject'] = Header(u'*** announcement from okinawa-taiki-scraper ***', 'utf-8')
    info['From'] = fr
    info['To'] = to
    # args can use string instead of MIMEText type.
    mail.sendmail(info["From"], info["To"], info.as_string())
    mail.quit()

