import argparse
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def read_secret_token():
    with open(os.path.join("..", ".bot_webhook_secret_token"), "r") as secret_token_file:
        return secret_token_file.read()


parser = argparse.ArgumentParser(description="Set Telegram bot webhook.")
parser.add_argument("--bot_token", type=str, help="Your Telegram bot token.", default=TELEGRAM_BOT_TOKEN)
parser.add_argument("--webhook_url", type=str, help="The URL for the webhook.", required=False)
parser.add_argument("--max-connections", type=str,
                    help="The maximum allowed number of simultaneous HTTPS connections",
                    default=10)
parser.add_argument("--secret-token", type=str,
                    help="""
                    A secret token to be sent in a header “X-Telegram-Bot-Api-Secret-Token” in every webhook request, 1-256 characters. 
                    Only characters A-Z, a-z, 0-9, _ and - are allowed. 
                    The header is useful to ensure that the request comes from a webhook set by you.
                    """,
                    default=read_secret_token())


def set_webhook(bot_token: str, webhook_url: str, max_connections: str, secret_token: str):
    api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    params = {"url": webhook_url, "max_connections": max_connections, "secret_token": secret_token}
    # print(f"setting webhooks using params: {params}")
    try:
        response = requests.post(api_url, params=params)
        print(f"Response received from setWebhook API: {response}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error setting webhook: {e}")
        return None


if __name__ == "__main__":
    args = parser.parse_args()

    webhook_url = args.webhook_url
    if not webhook_url:
        with open(os.path.join("..", "infra", "terraform_output.json"), "r", encoding="utf-8-sig") as tf_output_file:
            tf_output_vars: dict = json.load(tf_output_file)
            webhook_url = tf_output_vars.get("base_url", {}).get("value", "")

    result = set_webhook(args.bot_token,
                         webhook_url,
                         args.max_connections,
                         args.secret_token)
    if result:
        print("Webhook set successfully:", result)
    else:
        print("Failed to set webhook.")
