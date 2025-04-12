# Overview

- Want to create you own LLM Telegram bot?
- Want to know how to create a fully-serverless and secure Telegram webhook bot on AWS?

This project shows how to deploy and register a Telegram bot backed
by serverless AWS architecture. It exposes a secure API that act as a wrapper
for an LLM of choice.

## Features

This repository template demonstrates how to create the back-end infrastructure of a Telegram bot that is both **secure** and **cost-effective**.

Telegram bots can be deployed using the Webhook method. In this approach, when you send a message to the Telegram bot via the chat interface, Telegram forwards your message to a pre-configured REST API—this is your webhook.

In this repository, you will find:
- Infrastructure for creating a serverless API using AWS Lambda and API Gateway.
- An authentication setup that utilizes a Lambda authorizer and DynamoDB to:
  - Authenticate the request sender (ensuring requests come only from Telegram servers via a whitelisted IP).
  - Verify the Telegram user making the request is registered in a DynamoDB table.
- Python source code that implements a simple LLM Agent with an integrated web search tool (leveraging the Brave APIs).

## Architecture

![architecture.png](docs/imgs/architecture.jpg)

## Set Up Infrastructure and Telegram Bot

1. Create a telegram bot and obtain a **bot token** --> [CREATE_BOT.md](docs/CREATE_BOT.md)
2. Set up the infrastructure by running the Terraform script --> [SET_UP_INFRA.md](docs/SET_UP_INFRA.md)

## 📝 License

MIT License – see the [LICENSE](LICENSE) file for details.