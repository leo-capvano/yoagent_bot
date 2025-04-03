import json
import os
import traceback

import urllib3

from dto.error.FromError import FromNotPresentError
from dto.error.TextNotPresentError import TextNotPresentError
from dto.parser import parse_dto, parse_status_change
from dto.update import Update
from dynamodb_svc import is_user_allowed
from graph_svc import invoke_graph
from validation import is_authorization_secret_correct, is_bot_authorization_token_not_valid

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def lambda_handler(event, context):
    try:
        print(f"received event: {event}")

        if not is_authorization_secret_correct(event):
            print(f"Call not authorized - authorization secret not valid!")
            return exit_bot('Call not authorized! Authorization secret not valid!', 433)

        if is_bot_authorization_token_not_valid(event):
            print(f"Call not authorized - Telegram secret token invalid")
            return exit_bot('Call not authorized! Secret Token Invalid', 433)

        dto = json.loads(event['body'])

        status_change = parse_status_change(dto)
        if status_change:
            return handle_status_change(status_change)

        update_dto: Update = parse_dto(dto)
        if is_user_allowed(update_dto.message.message_from.user_id):

            print(f"*** chat id: {update_dto.message.chat.id}")
            print(f"*** user name: {update_dto.message.message_from.user_id}")
            print(f"*** message text: {update_dto.message.text}")
            print(json.dumps(dto))

            agent_response = invoke_graph(update_dto.message.text)

            send_reply(update_dto.message.chat.id, agent_response)
            return exit_bot("Message processed successfully", 200)
        else:
            print(
                f"Call not authorized - user {update_dto.message.message_from.user_id} is not authorized to use this bot!")
            send_reply(update_dto.message.chat.id,
                       "You are not authorized to use this bot, contact the administrator to register for use! Cacc e sord")
            return exit_bot(f"User {update_dto.message.message_from.user_id} not allowed to use this bot!", 298)
    except FromNotPresentError as fnpe:
        traceback.print_exc()
        send_reply(fnpe.get_message(), "Message type not supported")
        return exit_bot(fnpe.get_chat_id(), 298)
    except TextNotPresentError as tnpe:
        traceback.print_exc()
        send_reply(tnpe.get_chat_id(), "Only text messages are supported :/")
        return exit_bot(tnpe.get_message(), 298)
    except Exception as e:
        traceback.print_exc()
        print(f"Generic error: {e}")
        return exit_bot(f"Generic error: {e}", 299)


def handle_status_change(status_change) -> dict:
    print(f"Bot status changed in chat {status_change.chat.id}: {status_change.new_chat_member.status}")
    if status_change.new_chat_member.status == "kicked":
        print(f"Bot was removed from chat {status_change.chat.id}.")
    elif status_change.new_chat_member.status == "member":
        print(f"Bot was added to chat {status_change.chat.id}.")
    return exit_bot("Status change event processed successfully", 200)


def exit_bot(message: str, status_code: int) -> dict:
    return {
        'statusCode': status_code,
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
    body = {
        "message": {
            "chat": {
                "id": "local_chat_id"
            },
            "from": {
                "id": "you user id here to test"
            },
            "text": "ciao bot!"
        }
    }
    payload = {
        "body": json.dumps(body),
        "requestContext": {
            "authorizer": {
                "authorizationSecret": "local_auth_secret"
            }
        },
        "headers": {
            "X-Telegram-Bot-Api-Secret-Token": "local_bot_secret"
        }
    }
    response = lambda_handler(payload, None)
    print(f"Response: {response}")
