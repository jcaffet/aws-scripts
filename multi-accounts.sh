#!/bin/bash
# The aim of the script is the get a role on each account of the AWS Organizations service
ROLE=Administrator
TMP_ROLE_FILE=/tmp/assumerole.json
IDENTITY_ACCOUNT=123456123456
accounts=`aws organizations list-accounts | jq -r '.Accounts[] | select(.Status=="ACTIVE") | .Id'`


command-to-exec () {
  python3.7 iam/disable-unused-password.py
}

for account in ${accounts}; do
  if [ "${IDENTITY_ACCOUNT}" != "${account}" ]; then
    echo "Get role on ${account}"
    aws sts assume-role \
            --role-arn arn:aws:iam::${account}:role/${ROLE} \
            --role-session-name "RoleSession-${account}" > ${TMP_ROLE_FILE}
    export AWS_SECRET_ACCESS_KEY=`cat ${TMP_ROLE_FILE} | jq -r .Credentials.SecretAccessKey`
    export AWS_ACCESS_KEY_ID=`cat ${TMP_ROLE_FILE} | jq -r .Credentials.AccessKeyId`
    export AWS_SESSION_TOKEN=`cat ${TMP_ROLE_FILE} | jq -r .Credentials.SessionToken`
    if [ -n "${AWS_SECRET_ACCESS_KEY}" ] && [ -n "${AWS_ACCESS_KEY_ID}" ] && [ -n "${AWS_SESSION_TOKEN}" ]; then
       # you might include an aws cli command here ...
       command-to-exec 
    fi
    rm ${TMP_ROLE_FILE}
    unset AWS_SECRET_ACCESS_KEY
    unset AWS_ACCESS_KEY_ID
    unset AWS_SESSION_TOKEN
  else
    echo "Get role on ${account}"
    command-to-exec 
  fi
done

