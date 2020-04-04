#!/bin/bash
switch_role=`aws sts assume-role --role-arn "arn:aws:iam::638987496525:role/lambda_sqs_role" --role-session-name "lambda-role" > accessKey.json`
if [[ switch_role ]]; then
  export AWS_ACCESS_KEY_ID=$(cat accessKey.json | jq '.Credentials.AccessKeyId' | tr -d '"')
  export AWS_SECRET_ACCESS_KEY=$(cat accessKey.json | jq '.Credentials.SecretAccessKey' | tr -d '"')
  export AWS_SESSION_TOKEN=$(cat accessKey.json | jq '.Credentials.SessionToken' | tr -d '"')
fi
