import json
import os

import urllib3

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY = os.getenv("BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY",
                                                "X-Telegram-Bot-Api-Secret-Token")
BOT_WEBHOOK_SECRET_TOKEN = os.getenv("BOT_WEBHOOK_SECRET_TOKEN")


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


def lambda_handler(event, context):
    print(f"received event: {event}")
    print(f"received context: {context}")

    if ("headers" not in event or BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY not in event["headers"]
            or event["headers"][BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY] != BOT_WEBHOOK_SECRET_TOKEN):
        print(f"Call not authorized")
        return {
            'statusCode': 433,
            'body': json.dumps('Call not authorized! Secret Token Invalid')
        }

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
