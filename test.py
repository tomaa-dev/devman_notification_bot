import requests
from pprint import pprint
import time
import telegram
from decouple import config
import argparse


def main():
    dvmn_token = config('DVMN_TOKEN')
    tg_token = config('TG_BOT_TOKEN')
    tg_chat_id = config('TG_ID')
    bot = telegram.Bot(token=tg_token)

    parser = argparse.ArgumentParser(description='Программа отправляет уведомления')
    parser.add_argument('tg_id', help='id')
    args = parser.parse_args()
    chat_id = args.tg_id
    print(f"Ваш чат id {chat_id}")