#!/bin/bash
# The aim of the script is the get a role on each account of the AWS Organizations service
ROLE=Administrator
TMP_ROLE_FILE=/tmp/assumerole.json
accounts=`aws organizations list-accounts | jq -r '.Accounts[] | select(.Status=="ACTIVE") | .Id'`

for account in ${accounts}; do
  echo "Assume role on ${account}"
  aws sts assume-role \
          --role-arn arn:aws:iam::${account}:role/${ROLE} \
	  --role-session-name "RoleSession-${account}" > ${TMP_ROLE_FILE}
  export AWS_SECRET_ACCESS_KEY=`cat ${TMP_ROLE_FILE} | jq -r .Credentials.SecretAccessKey`
  export AWS_ACCESS_KEY_ID=`cat ${TMP_ROLE_FILE} | jq -r .Credentials.AccessKeyId`
  export AWS_SESSION_TOKEN=`cat ${TMP_ROLE_FILE} | jq -r .Credentials.SessionToken`
  # you might include an aws cli command here ...
  rm ${TMP_ROLE_FILE}
  unset AWS_SECRET_ACCESS_KEY
  unset AWS_ACCESS_KEY_ID
  unset AWS_SESSION_TOKEN
done
