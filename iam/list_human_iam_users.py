#!/usr/bin/python
# This script simply gives a list of human IAM users (IAM users with a password)
import boto3
import sys
from time import sleep
import csv

def main(argv):

   iam_client = boto3.client('iam')
   credential_report = get_credential_report(iam_client)

   for row in credential_report:
     if row['password_enabled'] == "true":
       print ("%s;%s" % (row['user'], row['password_last_used']))

def get_credential_report(iam_client):
    resp = iam_client.generate_credential_report()
    if resp['State'] == 'COMPLETE' :
        try: 
            response = iam_client.get_credential_report()
            credential_report_csv = response['Content']
            reader = csv.DictReader(credential_report_csv.splitlines())
            credential_report = []
            for row in reader:
                credential_report.append(row)
            return(credential_report)
        except ClientError as e:
            print("Unknown error getting Report: " + e.message)
    else:
        sleep(2)
        return get_credential_report(iam_client)

if __name__ == '__main__':
    main(sys.argv[1:])

