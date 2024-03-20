#!python3
# -*- coding:utf-8 -*-

import os
import csv

def save_csv(dic_data, file_name="./scrape_result.csv"):
    with open(file_name, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, ["kyoku_cd", "kyoku", "hour", "name", "value", "criteria"])
        writer.writeheader()
        writer.writerows(dic_data)
