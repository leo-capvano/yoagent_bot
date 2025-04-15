import json
import os
import threading
import time
from contextlib import contextmanager

import urllib3

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_reply(chat_id, message):
    call_api({
        "chat_id": chat_id,
        "text": message
    }, "sendMessage")


def set_typing(chat_id):
    call_api({
        "chat_id": chat_id,
        "action": "typing"
    }, "sendChatAction")


def call_api(payload: dict, operation: str):
    print(f"Calling API operation: {operation} with payload: {payload}")
    http = urllib3.PoolManager()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{operation}"
    encoded_data = json.dumps(payload).encode('utf-8')
    response = http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})
    print(f"*** API '{operation}' response: {response.json()}")


def ainvoke_set_typing(stop_event, chat_id):
    while not stop_event.is_set():
        set_typing(chat_id)
        time.sleep(4)


@contextmanager
def bot_is_typing(chat_id: str):
    stop_event = threading.Event()
    thread = threading.Thread(target=ainvoke_set_typing, args=(stop_event, chat_id))
    thread.start()
    try:
        yield
    finally:
        stop_event.set()
        thread.join()
        print("API polling stopped.")
