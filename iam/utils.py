'''
Generic usefull methods
Needs Python>=3.7 for fromisoformat usage
'''
from datetime import datetime, timezone
from time import sleep
import csv
from botocore.exceptions import ClientError


def get_credential_report(iam_client):
    '''
    Recursive function the generates a credentials report and waits for
    its final completion
    Credential Reports dates are in ISO8601 format like 2017-03-01T09:51:51+00:00
    Entries :
    iam_client : an IAM.Client class
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


def number_of_days_since_now_from_report_date(mydate):
    '''
    Calculates the number of days between today and the specifed date
    Entry : string ISO8601 format like 2017-03-01T09:51:51+00:00
    Returns a integer number
    '''
    if mydate == "no_information":
        return mydate
    else:
        return (datetime.now(timezone.utc) - datetime.fromisoformat(mydate)).days


def number_of_days_since_now_datetime(mydate: datetime):
    '''
    Calculates the number of days between today and the specifed date
    Entry : string ISO8601 format like 2017-03-01T09:51:51+00:00
    Returns a integer number
    '''
    if mydate is None:
        return 0
    return (datetime.now(timezone.utc) - mydate).days
