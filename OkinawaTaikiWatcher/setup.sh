#!/bin/bash
#  caution
#   このセットアップバッチはローカル環境へデプロイする場合にのみ有効です。
#   各クラウドサービスやレンタルサーバー上へデプロイする場合には各環境の公式手順書を参照してください。
#   前提条件：
#　　PCにPython3がインストールされていること。またpython3-venvがインストールされていること。
#

# venvが既にある場合は、いったん削除。
if [ -d ./venv ]; then
  rm -rf ./venv/.*
  rm -rf ./venv/*
  rmdir ./venv
fi

# venvを作成
mkdir venv
python3 -m venv venv

# venvを起動し、pipを最新へ更新
source ./venv/bin/activate
pip install -U pip

# 依存ライブラリのインストール
pip install -r requirements.txt

# venv環境を解除
deactivate
