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

    MAX_CREDENTIALS_AGE=90

    iam_client = boto3.client('iam')
    credential_report = get_credential_report(iam_client)
    for user_report in credential_report:
        remove_unused_password_access(iam_client, user_report, MAX_CREDENTIALS_AGE)


def remove_unused_password_access(iam_client, user_report, max_password_age):
    if user_report['password_enabled'] == "true":
        password_last_changed_age =  number_of_days_since_now(user_report['password_last_changed'])
        if password_last_changed_age > max_password_age:
            password_last_used_age  = number_of_days_since_now(user_report['password_last_used'])
            if (user_report['password_last_used'] == "no_information" or password_last_used_age > max_password_age):
                print ("Remove unused password till %d days of %s (last_changed : %s - %s days, last_used : %s - %s days)" % (max_password_age,
                                                                                                                             user_report['user'],
                                                                                                                             user_report['password_last_changed'],
                                                                                                                             password_last_changed_age,
                                                                                                                             user_report['password_last_used'],
                                                                                                                             password_last_used_age))
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
