import requests
from pprint import pprint
import time
import telegram
from decouple import config
import argparse


def main():
    dvmn_token = config('DVMN_TOKEN')
    tg_token = config('TG_BOT_TOKEN')
    bot = telegram.Bot(token=tg_token)

    parser = argparse.ArgumentParser(description='Программа отправляет уведомления о проверке работ на платформе Devman')
    parser.add_argument('tg_id', help='id')
    chat_id = parser.parse_args().tg_id

    headers = {
        "Authorization": f"Token {dvmn_token}"
    }

    url = "https://dvmn.org/api/long_polling/"
    current_timestamp = None


    while True:
        try:
            params = {}
            params["timestamp"] = current_timestamp
            response = requests.get(url, headers=headers,  params=params, timeout=2)

            response.raise_for_status()
            server_response = response.json()
            pprint(server_response)

            status = server_response.get("status")

            if status == "timeout":
                current_timestamp = server_response.get("timestamp_to_request")
            elif status == "found":
                current_timestamp = server_response.get("last_attempt_timestamp")

                new_attempts = server_response.get("new_attempts", [])
                for attempt in new_attempts:
                    lesson_title = attempt.get("lesson_title")
                    is_negative = attempt.get("is_negative")
                    lesson_url = attempt.get("lesson_url")

                    message_text = f"У вас проверили работу \"{lesson_title}\"\n\n"

                    if is_negative:
                        message_text += "К сожалению, в работе нашлись ошибки.\n\n"
                    else:
                        message_text += "Преподавателю все понравилось, можно приступать к следующему уроку!\n\n"
                    
                    message_text += f"Ссылка на урок: {lesson_url}."
                    bot.send_message(chat_id=chat_id, text=message_text)

        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            print('Подключение к серверу')
            time.sleep(10)


if __name__ == '__main__':
    main()