import os

import boto3

USERS_TABLE_NAME = os.getenv("USERS_TABLE_NAME")

users_table = boto3.resource("dynamodb").Table(USERS_TABLE_NAME)


def is_user_allowed(username: str) -> bool:
    """
    Check if the given user ID exists in the DynamoDB table.
    Returns True if the user is authorized, False otherwise.
    """
    try:
        response = users_table.get_item(Key={"username": username})
        return "Item" in response
    except Exception as e:
        print(f"Error checking user in DB: {e}")
        return False
