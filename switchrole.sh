#!/bin/bash
switch_role=`aws sts assume-role --role-arn "$1" --role-session-name "lambda-role" > accessKey.json`
if [[ switch_role ]]; then
  export AWS_ACCESS_KEY_ID=$(cat accessKey.json | jq '.Credentials.AccessKeyId' | tr -d '"')
  export AWS_SECRET_ACCESS_KEY=$(cat accessKey.json | jq '.Credentials.SecretAccessKey' | tr -d '"')
  export AWS_SESSION_TOKEN=$(cat accessKey.json | jq '.Credentials.SessionToken' | tr -d '"')
  aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
  aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
  aws configure set aws_session_token $AWS_SESSION_TOKEN
fi
