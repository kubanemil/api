#!/bin/bash

set -e

if [ $# -eq 0 ]; then
    echo "Error: No argument provided. Please specify the endpoint name."
    exit 1
fi

endpoint_name=$1

# Define variables
LAMBDA_FUNCTION_NAME=$endpoint_name
ZIP_FILE="$endpoint_name.zip"
PYTHON_FILE="$endpoint_name.py"
VIRTUAL_ENV_DIR="venv"
DEPLOYMENT_DIR="deployment_package"
IAM_ROLE_ARN="arn:aws:iam::010046428417:role/lambdaDB"
HANDLER_NAME="lambda_function.lambda_handler"
RUNTIME="python3.12"  

# Create a clean deployment directory
rm -rf $DEPLOYMENT_DIR
mkdir $DEPLOYMENT_DIR

# Activate the virtual environment
source $VIRTUAL_ENV_DIR/bin/activate

# Install dependencies in the deployment directory
pip install -r requirements.txt -t $DEPLOYMENT_DIR

# Deactivate the virtual environment
deactivate

# Copy the Python script to the deployment directory
cp endpoints/$PYTHON_FILE $DEPLOYMENT_DIR/lambda_function.py
cp endpoints/models.py $DEPLOYMENT_DIR/models.py

# Navigate to deployment directory
cd $DEPLOYMENT_DIR

# Zip all the contents including dependencies and the Python script
zip -r ../$ZIP_FILE .

# Navigate back to the original directory
cd ..

# Upload zip file to AWS Lambda
if aws lambda create-function --function-name $LAMBDA_FUNCTION_NAME \
    --zip-file fileb://$ZIP_FILE \
    --handler $HANDLER_NAME \
    --runtime $RUNTIME \
    --role $IAM_ROLE_ARN; then
    echo "Lambda function $LAMBDA_FUNCTION_NAME deployed successfully!"
else
    echo "Updating Lambda $endpoint_name..."
    aws lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME \
    --zip-file fileb://$ZIP_FILE
    echo "Lambda function $LAMBDA_FUNCTION_NAME is updated!"
fi

# Clear the temporary deployment package directory
rm -rf $DEPLOYMENT_DIR
rm -rf $ZIP_FILE