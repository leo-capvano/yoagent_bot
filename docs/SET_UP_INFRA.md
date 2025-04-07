# Register the Telegram Bot

## Overview
The file [telegram.py](../telegram/telegram.py) allows you to register a webhook using Telegram APIs. This enables your bot to receive and process messages through a REST API.

## How It Works
1. You already have a **REST API** that provides some functionality.
2. You **hook this REST API** to a Telegram bot.
3. You call a **Telegram API** to inform Telegram: 
   - "When a message is sent to this bot, forward it to my API for processing."
4. Telegram registers the webhook and starts forwarding messages to your API.

## Set Up environment files
Environment files are files that contains some values used by the system to implement
security, access to the LLM and to Telegram APIs.
In the project's root directory you can find:
- [.bot_token.example](../.bot_token.example) -> bot token given by @bot_father during bot creation
- [.bot_webhook_secret_token.example](../.bot_webhook_secret_token.example) -> contains a secret that Telegram servers will send inside the webhook request. It is used to verify that the request is sent by your Telegram API registration call (this value is included when you call the Telegram API to register the webhook)  
- [.llm_api_key.example](../.llm_api_key.example) -> contains the OPENAI_API_KEY's value that will be loaded by the bot. Support for other models can be added later
- [.authorization_secret.example](../.authorization_secret.example) -> the secret that is included when lambda authorizer forwards the request to the upstream. Double layered check to verify that the request is coming from lambda authorizer

Rename those files by removing the suffix **.example** and run .tf scripts.

## Steps to Set Up the Bot
### **1. Deploy the Infrastructure**
Run the **Terraform module** to create the necessary infrastructure, including the webhook REST API. You will need to input the **admin username**. This process also creates a secret that contains the **LLM API key** bound to the admin's Telegram username.

#### **Windows Command**
```sh
terraform destroy --auto-approve ; terraform apply -auto-approve; terraform output -json | Out-File -Encoding utf8 terraform_output.json
```
#### **Linux Command**
```sh
terraform destroy --auto-approve && terraform apply --auto-approve && terraform output -json > terraform_output.json
```
This command will:
- Destroy any existing infrastructure (if necessary).
- Deploy the new infrastructure.
- Generate a **terraform_output.json** file, which will be used in the next step.

### **2. Register the Webhook with Telegram**
Run the provided Python script to register the webhook:
```sh
python ../telegram/telegram.py
```

## Verify Webhook Registration
To check if the webhook is correctly registered, use the following Telegram API call:
```sh
https://api.telegram.org/bot<your_bot_token>/getWebhookInfo
```
Replace `<your_bot_token>` with your actual Telegram bot token.

---
### **Next Steps**
- Ensure your API is correctly handling Telegram messages.
- Test the webhook by sending a message to your bot.
- Monitor logs for any errors or misconfigurations.

Happy coding! 🚀