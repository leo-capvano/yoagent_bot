# How to Create a Telegram Bot Using BotFather

Telegram makes it easy to create your own bot using **BotFather**, the official Telegram bot used to manage all other bots.

## 🛠 Prerequisites

- A Telegram account
- The Telegram app installed on your phone or desktop

## 🤖 Steps to Create a Telegram Bot

### 1. Open a Chat with BotFather

- In Telegram, search for [@BotFather](https://t.me/BotFather)
- Open the chat and click **Start**

### 2. Create a New Bot

- Type `/newbot` and hit Enter
- BotFather will ask you to choose:
  - **Bot name**: This is your bot's display name (e.g., `My Weather Bot`)
  - **Username**: Must be unique and end with `bot` (e.g., `myweatherbot`)

### 3. Get the Bot Token

After creating the bot, BotFather will provide a **bot token**.

🔐 **Save this token inside [.bot_token.example](../.bot_token.example) and remove the .example suffix. You'll need it to control your bot through the Telegram Bot API.**

### 5. Start Using Your Bot

Your bot is now live! You can interact with it via its username (e.g., `@myweatherbot`) or start coding using the token and Telegram Bot API.

---

## 🧑‍💻 Example: Testing Your Bot with curl

You can quickly test your bot by sending a message using the Telegram API:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/sendMessage" \
     -d chat_id=<YOUR_CHAT_ID> \
     -d text="Hello from my bot!"

