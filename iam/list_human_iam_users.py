'''
This script simply gives a list of human IAM users (IAM users with a password)
'''
import sys
import boto3
import utils


def main(argv):

    iam_client = boto3.client('iam')
    awsaccountid = boto3.client('sts').get_caller_identity()['Account']

    credential_report = utils.get_credential_report(iam_client)
    for row in credential_report:
        if row['password_enabled'] == "true":
            print("%s;%s;%s" % (awsaccountid,
                                row['user'],
                                row['password_last_used']))


if __name__ == '__main__':
    main(sys.argv[1:])
