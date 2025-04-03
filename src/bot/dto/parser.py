import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from error.ChatError import ChatNotPresentError, ChatIdNotPresentError
from error.FromError import FromNotPresentError, FromIdNotPresentError
from error.MessageNotPresentError import MessageNotPresentError
from error.TextNotPresentError import TextNotPresentError
from update import Update, Message, Chat, MessageFrom, ChatMemberUpdated, ChatMember


def parse_dto(dto: dict) -> Update:
    if "message" not in dto:
        raise MessageNotPresentError(f"Message not present in input DTO: {dto}")

    if "chat" not in dto.get("message"):
        raise ChatNotPresentError(f"Chat not present in input DTO: {dto}")

    if "id" not in dto.get("message").get("chat"):
        raise ChatIdNotPresentError(f"Chat ID not present in input DTO: {dto}")

    chat_id = dto.get('message').get('chat').get('id')

    if "from" not in dto.get("message"):
        raise FromNotPresentError(f"From field in message not present in DTO: {dto}", chat_id)

    if "id" not in dto.get("message").get("from"):
        raise FromIdNotPresentError(f"From ID field in message not present in DTO: {dto}", chat_id)

    if "text" not in dto.get("message"):
        raise TextNotPresentError(f"Text not present in DTO: {dto}", chat_id)

    user_id = dto.get("message").get("from").get("id")
    message_text = dto.get("message").get("text")
    update_id = dto.get("update_id")

    message_from = MessageFrom(user_id=user_id)
    chat = Chat(id=chat_id)
    message = Message(text=message_text, chat=chat, message_from=message_from)
    return Update(update_id=update_id, message=message)


def parse_status_change(dto: dict) -> ChatMemberUpdated | None:
    try:
        if "my_chat_member" in dto:
            new_chat_member = ChatMember(status=dto["my_chat_member"]["new_chat_member"]["status"])
            chat = Chat(id=dto["my_chat_member"]["chat"]["id"])
            return ChatMemberUpdated(chat=chat, new_chat_member=new_chat_member)
    except Exception as e:
        print(f"Error while parsing status change dto. Error is: {e}")
        raise e
