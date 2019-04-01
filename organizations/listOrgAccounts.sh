#!/bin/sh
# List all active account with an AWS Organisation
# we assume the credentials are bound in the Organzations account, other use --profile option

accounts=`aws organizations list-accounts | jq -r '.Accounts[] |  select(.Status=="ACTIVE") | .Id'`

echo "Space separated accounts list :"
echo ${accounts}

COUNT=0
for accountId in ${accounts}; do
	if [ "${accountsCommaSeparated}" != "" ]; then
		accountsCommaSeparated="${accountsCommaSeparated},${accountId}"
		COUNT=$((COUNT+1))
	else
		accountsCommaSeparated="${accountId}"
		COUNT=$((COUNT+1))
	fi
done
echo "Comma separated accounts list :"
echo ${accountsCommaSeparated}
echo "${COUNT} accounts"
