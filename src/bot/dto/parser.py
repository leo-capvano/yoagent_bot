import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from update import Update, Message, Chat, MessageFrom, ChatMemberUpdated, ChatMember


def parse_dto(dto: dict) -> Update:
    try:
        chat_id = dto['message']['chat']['id']
        username = dto['message']['from']['username']
        message_text = dto['message']['text']
        update_id = dto["update_id"]

        message_from = MessageFrom(username=username)
        chat = Chat(id=chat_id)
        message = Message(text=message_text, chat=chat, message_from=message_from)
        return Update(update_id=update_id, message=message)
    except Exception as e:
        print(f"Error while parsing dto. Error is: {e}")


def parse_status_change(dto: dict) -> ChatMemberUpdated | None:
    try:
        if "my_chat_member" in dto:
            new_chat_member = ChatMember(status=dto["my_chat_member"]["new_chat_member"]["status"])
            chat = Chat(id=dto["my_chat_member"]["chat"]["id"])
            return ChatMemberUpdated(chat=chat, new_chat_member=new_chat_member)
    except Exception as e:
        print(f"Error while parsing status change dto. Error is: {e}")
