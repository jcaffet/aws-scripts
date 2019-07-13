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

    MAX_USER_AGE_WITH_MFA=14

    iam_client = boto3.client('iam')
    credential_report = get_credential_report(iam_client)
    for user_report in credential_report:
        if user_report['user'] != "<root_account>":
            remove_users_without_mfa(iam_client, user_report, MAX_USER_AGE_WITH_MFA)


def remove_users_without_mfa(iam_client, user_report, max_age_without_mfa):
    if user_report['password_enabled'] == "true" and user_report['mfa_active'] ==  "false":
            user_creation_age = number_of_days_since_now(user_report['user_creation_time'])
            if user_creation_age > max_age_without_mfa:
                print ("Remove user %s who has a password but no MFA till %d days (user_creation_time : %s - %s days)" % (user_report['user'],
                                                                                                                         max_age_without_mfa,
                                                                                                                         user_report['user_creation_time'],
                                                                                                                         user_creation_age))
                try:
                    response = iam_client.delete_login_profile(UserName=user_report['user'])
                except Exception as e:
                    if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                        print('User {} has no login profile'.format(user_report['user']))


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