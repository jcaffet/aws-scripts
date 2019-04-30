#!/usr/bin/python
# Pay attention that credential reports are renewed by AWS every 4 hours.
# Credential Reports provide date in ISO8601 format like 2017-03-01T09:51:51+00:00
# To convert to datetime, with use an out of the box function new in Python 3.7
import boto3
from botocore.exceptions import ClientError
import sys
import datetime
from datetime import datetime, timezone
from time import sleep
import csv
import base64


def main(argv):

    MAX_ACCESSKEY_AGE=180

    iam_client = boto3.client('iam')
    AwsAccountId = boto3.client('sts').get_caller_identity()['Account']
    credential_report = get_credential_report(iam_client)
    for user_report in credential_report:
        if user_report['user'] != "<root_account>":
            remove_not_rotated_accesskeys(iam_client, user_report['user'], MAX_ACCESSKEY_AGE, AwsAccountId)


def remove_not_rotated_accesskeys(iam_client, username, max_accesskey_age, my_account):
    response = iam_client.list_access_keys(UserName = username)
    for accesskey in response['AccessKeyMetadata']:
        accesskey_create_date = accesskey['CreateDate']
        accesskey_create_age = (datetime.now(timezone.utc) - accesskey_create_date).days
        if accesskey_create_age > max_accesskey_age:
            print("%s - Remove %s accesskey not rotated till %d days of %s (creation : %s - %s days)" % (my_account,
                                                                                                    accesskey['AccessKeyId'],
                                                                                                    max_accesskey_age,
                                                                                                    username,
                                                                                                    accesskey_create_date,
                                                                                                    accesskey_create_age))
            #iam_client.delete_access_key(UserName = username, AccessKeyId = accesskey['AccessKeyId'])


def get_credential_report(iam_client):
    resp = iam_client.generate_credential_report()
    if resp['State'] == 'COMPLETE' :
        try:
            response = iam_client.get_credential_report()
            credential_report_csv = response['Content']
            reader = csv.DictReader(credential_report_csv.decode('utf-8').splitlines())
            credential_report = []
            for row in reader:
                credential_report.append(row)
            return(credential_report)
        except ClientError as e:
            print("Error getting Report: " + e.message)
    else:
        sleep(2)
        return get_credential_report(iam_client)


def number_of_days_since_now(mydate):
    # The incoming mydate is in String type and could contain "no_information" values
    # fromisoformat only exists since Python 3.7
    if mydate == "no_information":
        return mydate
    else:
        return (datetime.now(timezone.utc) - datetime.fromisoformat(mydate)).days


if __name__ == '__main__':
    main(sys.argv[1:])
