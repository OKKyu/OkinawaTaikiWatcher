#!/bin/sh

# venv環境をロード
source ./venv/bin/activate

# 自動取得・通知処理スクリプトを実行する
cd ./
python scraping_okinawa-taiki.py

# venv環境を解除
deactivate


