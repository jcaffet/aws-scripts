'''
Pay attention that credential reports are renewed by AWS every 4 hours.
CredentialReport provides ISO8601 dates format like 2017-03-01T09:51:51+00:00
To convert to datetime, with use an out of the box function new in Python 3.7
'''
import boto3
import sys
from datetime import datetime, timezone
import utils


def main(argv):

    max_accesskey_age = 180

    iam_client = boto3.client('iam')
    awsaccountid = boto3.client('sts').get_caller_identity()['Account']
    credential_report = utils.get_credential_report(iam_client)
    for user_report in credential_report:
        if user_report['user'] != "<root_account>":
            remove_not_rotated_accesskeys(iam_client,
                                          user_report['user'],
                                          max_accesskey_age,
                                          awsaccountid)


def remove_not_rotated_accesskeys(iam_client, username, max_accesskey_age, my_account):
    response = iam_client.list_access_keys(UserName=username)
    for accesskey in response['AccessKeyMetadata']:
        accesskey_create_date = accesskey['CreateDate']
        accesskey_create_age = utils.number_of_days_since_now_datetime(accesskey_create_date)
        if accesskey_create_age > max_accesskey_age:
            print("%s - Remove %s accesskey not rotated till %d days of %s (creation : %s - %s days)" % (my_account,
                                                                                                    accesskey['AccessKeyId'],
                                                                                                    max_accesskey_age,
                                                                                                    username,
                                                                                                    accesskey_create_date,
                                                                                                    accesskey_create_age))
            #iam_client.delete_access_key(UserName = username, AccessKeyId = accesskey['AccessKeyId'])


if __name__ == '__main__':
    main(sys.argv[1:])
