#!/bin/bash
# The aim of the script is the get a role on each account of the AWS Organizations service
# Do nto forget to specify your parameters (ROLE and IDENTITY_ACCOUNT)
ROLE=Administrator
TMP_ROLE_FILE=/tmp/assumerole.json
IDENTITY_ACCOUNT=
accounts=`aws organizations list-accounts | jq -r '.Accounts[] | select(.Status=="ACTIVE") | .Id'`
regions=`aws ec2 describe-regions | jq -r '.Regions[] | .RegionName'`

command-to-exec () {
  # your command here
  echo "${account}:${region}"
}

for account in ${accounts}; do
  if [ "${IDENTITY_ACCOUNT}" != "${account}" ]; then
    aws sts assume-role \
            --role-arn arn:aws:iam::${account}:role/${ROLE} \
            --role-session-name "RoleSession-${account}" \
	    > ${TMP_ROLE_FILE}
    export AWS_SECRET_ACCESS_KEY=`cat ${TMP_ROLE_FILE} | jq -r .Credentials.SecretAccessKey`
    export AWS_ACCESS_KEY_ID=`cat ${TMP_ROLE_FILE} | jq -r .Credentials.AccessKeyId`
    export AWS_SESSION_TOKEN=`cat ${TMP_ROLE_FILE} | jq -r .Credentials.SessionToken`
    if [ -n "${AWS_SECRET_ACCESS_KEY}" ] && [ -n "${AWS_ACCESS_KEY_ID}" ] && [ -n "${AWS_SESSION_TOKEN}" ]; then
       for region in ${regions}; do
           export AWS_DEFAULT_REGION=${region}
           command-to-exec
       done
    fi
    rm ${TMP_ROLE_FILE}
    unset AWS_SECRET_ACCESS_KEY
    unset AWS_ACCESS_KEY_ID
    unset AWS_SESSION_TOKEN
    unset AWS_DEFAULT_REGION
  else
    command-to-exec
  fi
done
