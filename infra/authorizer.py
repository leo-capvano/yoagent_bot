import os

BOT_WEBHOOK_SECRET_TOKEN = os.getenv("BOT_WEBHOOK_SECRET_TOKEN")
BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY = os.getenv("BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY",
                                                "X-Telegram-Bot-Api-Secret-Token")
AUTHORIZATION_SECRET = os.getenv("AUTHORIZATION_SECRET")


def lambda_handler(event, context):
    print("START Lambda Authorizer ...")
    print(f"received event: {event}")
    print(f"received context: {context}")

    if "headers" not in event or BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY not in event["headers"]:
        print("Lambda Authorizer - Call not authorized! API Key missing")
        return deny_request()
    return allow_request()


def deny_request():
    return {
        "principalId": "*",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "*",
                    "Effect": "Deny",
                    "Resource": "*"
                }
            ]
        }
    }


def allow_request():
    return {
        "principalId": "*",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": "*"
                }
            ]
        },
        "context": {
            "authorizationSecret": AUTHORIZATION_SECRET
        },
        "usageIdentifierKey": BOT_WEBHOOK_SECRET_TOKEN
    }
