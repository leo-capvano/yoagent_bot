# Upgrade Dependencies
The bot is implemented using a lambda function that needs some dependencies. 
The Dependencies are packaged into a lambda layer [bot_layer.zip](..%2Finfra%2Flayer%2Fbot_layer.zip)

If you need to upgrade some dependencies just regenerate the layer:
1. pip install --platform manylinux2014_x86_64 --target=layer\python\lib\python3.12\site-packages\ --only-binary=:all:  langchain langgraph langchain-openai [...]
2. zip the content of layer\python\lib\python3.12\site-packages\ into a zip named bot_layer.zip
3. done, apply terraform
