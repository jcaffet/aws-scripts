#!/bin/sh
# List all active account with an AWS Organisation
# we assume the credentials are bound in the Organzations account, other use --profile option

accounts=`aws organizations list-accounts | jq -r '.Accounts[] |  select(.Status=="ACTIVE") | .Id'`
for accountId in ${accounts}; do
  accountsCommaSeparated="${accountsCommaSeparated},${accountId}"
done
echo ${accountsCommaSeparated}

