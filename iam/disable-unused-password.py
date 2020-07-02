'''
Pay attention that credential reports are renewed by AWS every 4 hours.
Credential Reports return date in ISO8601 format like 2017-03-01T09:51:51+00:00
To convert to datetime, with use an out of the box function new in Python 3.7
'''
import sys
import boto3
import utils


def main(argv):

    max_credentials_age = 90

    iam_client = boto3.client('iam')
    credential_report = utils.get_credential_report(iam_client)
    for user_report in credential_report:
        remove_unused_password_access(iam_client, user_report, max_credentials_age)


def remove_unused_password_access(iam_client, user_report, max_password_age):
    if user_report['password_enabled'] == "true":
        password_last_changed_age = utils.number_of_days_since_now_from_report_date(user_report['password_last_changed'])
        if password_last_changed_age > max_password_age:
            password_last_used_age = utils.number_of_days_since_now_from_report_date(user_report['password_last_used'])
            if (user_report['password_last_used'] == "no_information" or password_last_used_age > max_password_age):
                print("Remove unused password till %d days of %s (last_changed : %s - %s days, last_used : %s - %s days)" % (max_password_age,
                                                                                                                             user_report['user'],
                                                                                                                             user_report['password_last_changed'],
                                                                                                                             password_last_changed_age,
                                                                                                                             user_report['password_last_used'],
                                                                                                                             password_last_used_age))
                try:
                    iam_client.delete_login_profile(UserName=user_report['user'])
                except Exception as e:
                    if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                        print('User {} has no login profile'.format(user_report['user']))


if __name__ == '__main__':
    main(sys.argv[1:])
