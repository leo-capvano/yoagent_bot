# Register the bot
The file [telegram.py](..%2Ftelegram%2Ftelegram.py) allows you to register a webhook
using Telegram APIs.

How doest it works:
1. suppose you already have a REST API that exposes some functionality, you can hook 
this REST API to a telegram bot
2. you can call a Telegram API to tell Telegram "Hey, when you receive a message to **this** bot, forward it to this API 
that will handle the response"
3. Telegram will register it and all the messages to the bot will be sent to the API

You just have to:
1. execute the Terraform Module to create the infrastructure (Webhook REST API). 
Remember to input the admin username; the script will create a secret containing the LLM API key bound to the admin Telegram username 
(e.g. for **@myTelegramUsername** input **myTelegramUsername**)
> (for Winodws)  
> terraform destroy --auto-approve ; terraform apply -auto-approve; terraform output -json | Out-File -Encoding utf8 terraform_output.json
2. execute the given python script [telegram.py](..%2Ftelegram%2Ftelegram.py)