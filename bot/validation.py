import os

AUTHORIZATION_SECRET = os.getenv("AUTHORIZATION_SECRET")
BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY = os.getenv("BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY",
                                                "X-Telegram-Bot-Api-Secret-Token")
BOT_WEBHOOK_SECRET_TOKEN = os.getenv("BOT_WEBHOOK_SECRET_TOKEN")


def is_authorization_secret_correct(event: dict):
    received_authorization_secret = (event.get("requestContext", {})
                                     .get("authorizer", {})
                                     .get("authorizationSecret", ""))
    if received_authorization_secret != AUTHORIZATION_SECRET:
        return False
    return True


def is_bot_authorization_token_valid(event):
    return "headers" not in event or BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY not in event["headers"] or event["headers"][
        BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY] != BOT_WEBHOOK_SECRET_TOKEN
