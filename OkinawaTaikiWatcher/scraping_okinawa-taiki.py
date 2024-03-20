#! python3
# -*- coding:utf-8 -*-
import os
import sys
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta, timezone
from lib.db import select_t_taiki, insert_t_taiki, update_t_taiki, delete_t_taiki
from lib.db import create_t_taiki, select_t_criterias_all, select_t_settings, select_t_taiki_justbefore, select_t_kyokus_all, update_t_taiki_alerted
# from lib.save_csv import save_csv
# from lib.mail import send_smtp
from lib.line import send_line

# basical setting
base_url = "https://okinawa-taiki.sakura.ne.jp/kyoku"
db_path = "./db/okinawa-taiki.sqlite3"
db_path2 = "./db/admin.sqlite3"

# check wether boot can allow.
setting_params = []
alert_on = False
if Path(db_path2).exists() is True:
    setting_params = select_t_settings(db_path2)
    alert_on = bool(setting_params[1])
else:
    alert_on = True


# create database for data store
if Path(db_path).exists() is not True:
    create_t_taiki(db_path)

# criteria.
if Path(db_path2).exists() is True:
    criterias = select_t_criterias_all(db_path2)
else:
    # dummy criterias for test.
    criterias = {"SO2": 0.0001, "NO": 0.0009, "NO2": 12, "NOX": 13, "CO": 14, "OX": 15, "NMHC": 16, "CH4": 17, "SPM": 18, "PM2.5": 19}

# kyokus and exculded kyokus.
list_sokutei_kyokus = []
list_sokutei_kyokus_exclude = []
if Path(db_path2).exists() is True:
    kyokus_all = select_t_kyokus_all(db_path2)
    for name, val in kyokus_all.items():
        if bool(val[2]) is False:
            list_sokutei_kyokus_exclude.append(name)
else:
    # dummy excluded kyokus for test.
    list_sokutei_kyokus_exclude = ["石垣", "宮古"]


# mail setting
'''  
host = "smtp.gmail.com"
port = 587
login_mail = ""
login_pw = ""
fr_mail_addr = ""
to_mail_addr = ""
'''

# start main process
start_time = datetime.now(timezone(timedelta(hours=9)))
start_time_ymd = str(start_time.year) + str(start_time.month).rjust(2, "0") + str(start_time.day).rjust(2, "0")
start_time_hour = str(start_time.hour) + "時"

print("scraping_okinawa-taiki start " + start_time.strftime("%Y%m%d %H:%M:%S"))

# for the first, get kyoku's code from web page.
response1 = requests.get(base_url)
if response1.status_code != 200:
    print("oh, https request error has occured...")
    print("Getting kyoku\'s code was failure... exit this operation.")
    print("status_code : " + str(response.status_code))
    sys.exit(1)

parser1 = BeautifulSoup(response1.content, "html.parser")
parser1_kyoku_options = parser1.select("select#kyoku option")

# set some pare of kyoku's name and kyoku's code into list.
for op in parser1_kyoku_options:
    list_sokutei_kyokus.append([op.text, op.get("value")])

# This argument is for packing all alert message that be sended to LINE.
message_over = ""
message_hyphen = ""

for kyoku in list_sokutei_kyokus:
    # make parameter for getting requested web page.
    post_params = {"kyoku": kyoku[1],
                   "date": start_time.strftime("%Y%m%d"),
                   "operation": "non"
                   }

    # get web page which including air pollusion datas.
    response2 = requests.post(base_url, post_params)

    # If you got web page, start converting data and send message.
    if response2.status_code == 200:
        parser2 = BeautifulSoup(response2.content, "html.parser")
        headers = parser2.select("table thead div.enk")
        datarows = parser2.select("table tbody tr")

        # fetch all rows (from 1 to 24 hour)
        for datarow in datarows:
            # If the hour which in datarow is match to target hour, start convert.
            if datarow.th.text == start_time_hour:
                report_datas = []

                tds = datarow.select("td")
                for data in zip(headers, tds):
                    tx_name = data[0].text
                    tx_val = data[1].text

                    # get one data in datarow.
                    d = {"kyoku_cd": kyoku[1], "kyoku": kyoku[0], "date": start_time_ymd, "hour": start_time_hour, "name": tx_name, "value": tx_val, "criteria": str(criterias.get(tx_name, "None"))}
                    # temporary saving for export to csv after.
                    report_datas.append(d)

                    # save to sqlite.
                    # save current value and info into sqlite.
                    before_up_rec = None
                    r = insert_t_taiki(db_path, [d.get("kyoku"), d.get("date"), d.get("hour"), d.get("name"), d.get("value"), d.get("criteria")])
                    if r == 2:
                        # if insert is error, do update.
                        before_up_rec = select_t_taiki(db_path, [d.get("kyoku"), d.get("date"), d.get("hour"), d.get("name")])
                        update_t_taiki(db_path, [d.get("kyoku"), d.get("date"), d.get("hour"), d.get("name"), d.get("value"), d.get("criteria")])

                    '''
                      judge and make alert message phase.
                         if kyoku is one of should be excluding, skip alert.
                         if alert_on flg is false(off), skip alert.
                         if alterted_flg in record is true, skip alert.
                    '''
                    if alert_on is False or (kyoku[0] in list_sokutei_kyokus_exclude) is True or \
                       (before_up_rec is not None and before_up_rec[6] == 1):
                        continue
                    # preprocess for judging.
                    tx_val = tx_val.replace("-", "")
                    tx_val = tx_val.replace("*", "")

                    #  judge1:value is over criteria
                    #  check wether current value is exists or not.
                    if len(tx_val) > 0:
                        '''
                          judge current value has changed to compare to recent value.
                          pattern that be checked is below.
                            current : recent
                            float  : -
                            float  : *
                            float  : float(same)
                            float  : float(different)
                        '''
                        tx_val = float(tx_val)
                        # Judge either value bigger than criteria.
                        if tx_val is not None and d.get("criteria") is not None and tx_val >= float(d.get("criteria")):
                            if len(message_over) <= 0:
                                message_over += "*** announcement from okinawa-taiki-scraper ***" + os.linesep
                                message_over += "閾値を超えた物質があります。" + os.linesep
                                message_over += "局：物質：測定値>=基準値" + os.linesep
                            message_over += d.get("kyoku") + "：" + d.get("name") + "：" + d.get("value") + ">=" + d.get("criteria") + os.linesep
                            update_t_taiki_alerted(db_path, [d.get("kyoku"), d.get("date"), d.get("hour"), d.get("name"), 1])

                    #  judge2: "-" value appear and just before value is numeric?
                    if d.get("value") is not None and d.get("value") == "-":
                        rec = select_t_taiki_justbefore(db_path, [d.get("kyoku"), d.get("name")])
                        if rec is not None and rec[4] != "-":
                            if len(message_hyphen) <= 0:
                                message_hyphen += "以下の局（地点）では値の欠測が発生しました。" + os.linesep
                            message_hyphen += d.get("kyoku") + "：" + d.get("name") + os.linesep
                            update_t_taiki_alerted(db_path, [d.get("kyoku"), d.get("date"), d.get("hour"), d.get("name"), 1])

    else:
        print("oh, https request error has occured...")
        print("status_code : " + str(response.status_code))

# message sending phase.
if len(message_over + message_hyphen) > 0 and alert_on is True:
    msg_merge = ""
    if len(message_over) > 0:
        msg_merge += message_over
    if len(message_over) > 0:
        msg_merge += message_hyphen

    # if line-notify's token was setted, send to it.
    if os.environ.get("LINE_NOTIFY_ACCESS_TOKEN", None) is not None:
        send_line(msg_merge)
    # if mail address was setted, send to it.
    # no coding while major version 1.
    # if :
    #    pass


print("scraping_okinawa-taiki end " + datetime.now(timezone(timedelta(hours=9))).strftime("%Y%m%d %H:%M:%S"))
