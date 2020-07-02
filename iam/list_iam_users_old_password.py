'''
This script simply gives a list of IAM users with a password age old than
the max defined
Pay attention that credential reports are renewed by AWS every 4 hours.
'''
import sys
import boto3
import utils


def main(argv):

    # 6 months max age
    max_password_age = 180

    iam_client = boto3.client('iam')
    credential_report = utils.get_credential_report(iam_client)

    print("user;password_age")
    for row in credential_report:
        if row['password_enabled'] == "true":
            password_age = utils.number_of_days_since_now_from_report_date(row['password_last_changed'])
            if password_age > max_password_age:
                print("%s;%s" % (row['user'], password_age))


if __name__ == '__main__':
    main(sys.argv[1:])
