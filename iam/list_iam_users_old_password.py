'''
This script simply gives a list of IAM users with a password age old than
the max defined
Pay attention that credential reports are renewed by AWS every 4 hours.
Credential Reports dates are in ISO8601 format like 2017-03-01T09:51:51+00:00

To convert to datetime, with use an out of the box function new in Python 3.7
'''
import sys
from datetime import datetime, timezone
from time import sleep
import csv
import boto3
from botocore.exceptions import ClientError


def main(argv):

    # 6 months max age
    max_password_age = 180

    iam_client = boto3.client('iam')
    credential_report = get_credential_report(iam_client)

    for row in credential_report:
        if row['password_enabled'] == "true":
            password_age = number_of_days_since_now(row['password_last_changed'])
            if password_age > max_password_age:
                print("%s;%s" % (row['user'], password_age))


def get_credential_report(iam_client):
    '''
    Recursive function the generates a credentials report and waits for
    its final completion
    '''
    resp = iam_client.generate_credential_report()
    if resp['State'] == 'COMPLETE':
        try:
            response = iam_client.get_credential_report()
            credential_report_csv = response['Content']
            reader = csv.DictReader(credential_report_csv.decode('utf-8').splitlines())
            credential_report = []
            for row in reader:
                credential_report.append(row)
            return credential_report
        except ClientError as e:
            print("Error getting Report: " + e)
    else:
        sleep(2)
        return get_credential_report(iam_client)


def number_of_days_since_now(mydate):
    '''
    The incoming mydate is in String type and could contain "no_information"
    fromisoformat only exists since Python 3.7
    '''
    if mydate == "no_information":
        return mydate
    else:
        return (datetime.now(timezone.utc) - datetime.fromisoformat(mydate)).days


if __name__ == '__main__':
    main(sys.argv[1:])
