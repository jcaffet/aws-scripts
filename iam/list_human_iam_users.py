'''
This script simply gives a list of human IAM users (IAM users with a password)
Need Python >= 3.6
'''
import sys
from time import sleep
import csv
import boto3
from botocore.exceptions import ClientError


def main(argv):

    iam_client = boto3.client('iam')
    awsaccountid = boto3.client('sts').get_caller_identity()['Account']

    credential_report = get_credential_report(iam_client)
    for row in credential_report:
        if row['password_enabled'] == "true":
            print("%s;%s;%s" % (awsaccountid,
                                row['user'],
                                row['password_last_used']))


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


if __name__ == '__main__':
    main(sys.argv[1:])
