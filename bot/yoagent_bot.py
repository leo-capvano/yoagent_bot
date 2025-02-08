import json
import os

import urllib3

from validation import is_authorization_secret_correct, is_bot_authorization_token_valid

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def lambda_handler(event, context):
    print(f"received event: {event}")
    print(f"received context: {context}")

    if not is_authorization_secret_correct(event):
        print(f"Call not authorized - authorization secret not valid!")
        return not_authorized('Call not authorized! Authorization secret not valid!')

    if is_bot_authorization_token_valid(event):
        print(f"Call not authorized - Telegram secret token invalid")
        return not_authorized('Call not authorized! Secret Token Invalid')

    body = json.loads(event['body'])
    chat_id = body['message']['chat']['id']
    user_name = body['message']['from']['username']
    message_text = body['message']['text']

    print(f"*** chat id: {chat_id}")
    print(f"*** user name: {user_name}")
    print(f"*** message text: {message_text}")
    print(json.dumps(body))

    reply_message = f"Reply to {message_text}"
    send_reply(chat_id, reply_message)
    return {
        'statusCode': 200,
        'body': json.dumps('Message processed successfully')
    }


def not_authorized(message: str):
    return {
        'statusCode': 433,
        'body': json.dumps(message)
    }


def send_reply(chat_id, message):
    reply = {
        "chat_id": chat_id,
        "text": message
    }

    http = urllib3.PoolManager()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    encoded_data = json.dumps(reply).encode('utf-8')
    http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})

    print(f"*** Reply : {encoded_data}")
