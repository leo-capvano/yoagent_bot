import boto3


def get_secret(secret_id: str):
    client = boto3.session.Session().client(service_name='secretsmanager')
    get_secret_value_response = client.get_secret_value(SecretId=secret_id)
    return get_secret_value_response['SecretString']
