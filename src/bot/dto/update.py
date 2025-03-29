from dataclasses import dataclass


@dataclass
class MessageFrom:
    username: str


@dataclass
class Chat:
    id: str


@dataclass
class Message:
    chat: Chat
    message_from: MessageFrom
    text: str


@dataclass
class Update:
    update_id: int
    message: Message


@dataclass
class ChatMember:
    status: str


@dataclass
class ChatMemberUpdated:
    chat: Chat
    new_chat_member: ChatMember
