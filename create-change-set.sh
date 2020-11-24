#!/bin/bash

CHANGESET_OPTION=--no-execute-changeset

if [ $# -gt 1 ]; then
  echo 'Usage : create-change-set [deploy]'
  exit
fi

if [ $# = 1 ]; then
  if [ $1 = "deploy" ]; then
    CHANGESET_OPTION=""
  else
    echo 'Usage "create-change-set [deploy]'
    exit
  fi
fi

# スタック名
CFN_STACK_NAME=management-event-trail

# テンプレートファイル
CFN_TEMPLATE=template.yml

# パラメータファイル
CFN_TEMPLATE_PARAMETER=parameters.json

# ChangeSetの作成
aws cloudformation deploy \
  --stack-name ${CFN_STACK_NAME} \
  --template-file ${CFN_TEMPLATE} \
  --parameter-overrides `jq -r '.Parameters|to_entries|map("\(.key)=\(.value|tostring)")|.[]' ${CFN_TEMPLATE_PARAMETER}` \
  --capabilities CAPABILITY_NAMED_IAM \
  ${CHANGESET_OPTION}

