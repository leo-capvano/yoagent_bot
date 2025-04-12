# Upgrade Bot Dependencies

## Overview
The bot is implemented using a Lambda function, which relies on several dependencies packaged into a Lambda layer. The dependencies are currently bundled in a zip file called [bot_layer.zip](../infra/layer/bot_layer.zip).

If you need to **upgrade** the dependencies, follow the steps below to regenerate the Lambda layer with the updated packages.

## Steps to Upgrade Dependencies
### **1. Install Dependencies**
Use `pip` to install the updated dependencies, specifying the `manylinux2014` platform to ensure compatibility with AWS Lambda.

Run the following command (adjusting the packages as needed):
```sh
pip install --platform manylinux2014_x86_64 --target=../infra/layer/requirements_layer/python/lib/python3.12/site-packages/ --only-binary=:all: -r ../src/requirements.txt
```
Requirements file: [requirements.txt](../src/requirements.txt)
This installs the required dependencies into the correct folder structure for Lambda.

### **2. Package the Dependencies**
After installing the dependencies, zip the contents of the `infra/layer/requirements_layer/python/lib/python3.12/site-packages/` folder into a new **requirements_layer.zip**.
```sh
zip -r ../infra/layer/requirements_layer.zip ..infra/layer/requirements_layer/python/lib/python3.12/site-packages/*
```
Make sure all the files from the `site-packages/` folder are included in the zip archive.


### **3. Apply Terraform**
Once the updated `requirements_layer.zip` is ready, apply the Terraform configuration to deploy the updated layer to AWS Lambda.
```sh
terraform apply -auto-approve
```
This will update the Lambda function with the new dependencies.

## Conclusion
The Lambda function will now use the upgraded dependencies. Be sure to test the bot functionality after the update to confirm everything is working as expected.

---
### **Next Steps**
- Test the updated Lambda function.
- Monitor logs to ensure the new dependencies are working correctly.

Happy coding! 🚀