import json
import os

import urllib3

from dto.parser import parse_dto, parse_status_change
from dto.update import Update
from dynamodb_svc import is_user_allowed
from secrets_manager_svc import get_secret
from validation import is_authorization_secret_correct, is_bot_authorization_token_not_valid

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def lambda_handler(event, context):
    print(f"received event: {event}")
    print(f"received context: {context}")

    if not is_authorization_secret_correct(event):
        print(f"Call not authorized - authorization secret not valid!")
        return not_authorized('Call not authorized! Authorization secret not valid!')

    if is_bot_authorization_token_not_valid(event):
        print(f"Call not authorized - Telegram secret token invalid")
        return not_authorized('Call not authorized! Secret Token Invalid')

    dto = json.loads(event['body'])

    status_change = parse_status_change(dto)
    if status_change:
        return handle_status_change(status_change)

    update_dto: Update = parse_dto(dto)
    if is_user_allowed(update_dto.message.message_from.username):
        llm_api_key = get_secret("llm_api_key")

        print(f"*** chat id: {update_dto.message.chat.id}")
        print(f"*** user name: {update_dto.message.message_from.username}")
        print(f"*** message text: {update_dto.message.text}")
        print(f"*** llm api key {llm_api_key}")
        print(json.dumps(dto))

        reply_message = f"Reply to {update_dto.message.text}"
        send_reply(update_dto.message.chat.id, reply_message)
        return {
            'statusCode': 200,
            'body': json.dumps('Message processed successfully')
        }
    else:
        print(
            f"Call not authorized - user {update_dto.message.message_from.username} is not authorized to use this bot!")
        send_reply(update_dto.message.chat.id,
                   "You are not authorized to use this bot, contact the administrator to register for use! Cacc e sord")
        return not_authorized(f"User {update_dto.message.message_from.username} not allowed to use this bot!")


def handle_status_change(status_change) -> dict:
    print(f"Bot status changed in chat {status_change.chat.id}: {status_change.new_chat_member.status}")
    if status_change.new_chat_member.status == "kicked":
        print(f"Bot was removed from chat {status_change.chat.id}.")
    elif status_change.new_chat_member.status == "member":
        print(f"Bot was added to chat {status_change.chat.id}.")
    return {
        'statusCode': 200,
        'body': json.dumps('Status change event processed successfully')
    }


def not_authorized(message: str) -> dict:
    return {
        'statusCode': 299,
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


if __name__ == '__main__':
    lambda_handler(None, None)
