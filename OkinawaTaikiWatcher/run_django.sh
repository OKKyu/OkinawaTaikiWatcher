#!/bin/sh

# venv環境をロード
source ./venv/bin/activate

# 管理画面用Djangoを実行する
cd ./
python manage.py runserver

# venv環境を解除
deactivate


