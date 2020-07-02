'''
Pay attention that credential reports are renewed by AWS every 4 hours.
Credential Reports return date in ISO8601 format like 2017-03-01T09:51:51+00:00
To convert to datetime, with use an out of the box function new in Python 3.7
'''
import sys
import boto3
import utils


def main(argv):

    max_user_age_with_mfa = 14

    iam_client = boto3.client('iam')
    credential_report = utils.get_credential_report(iam_client)
    for user_report in credential_report:
        if user_report['user'] != "<root_account>":
            remove_users_without_mfa(iam_client, user_report, max_user_age_with_mfa)


def remove_users_without_mfa(iam_client, user_report, max_age_without_mfa):
    if user_report['password_enabled'] == "true" and user_report['mfa_active'] ==  "false":
            user_creation_age = utils.number_of_days_since_now_from_report_date(user_report['user_creation_time'])
            if user_creation_age > max_age_without_mfa:
                print ("Remove user %s who has a password but no MFA till %d days (user_creation_time : %s - %s days)" % (user_report['user'],
                                                                                                                         max_age_without_mfa,
                                                                                                                         user_report['user_creation_time'],
                                                                                                                         user_creation_age))
                try:
                    iam_client.delete_login_profile(UserName=user_report['user'])
                except Exception as e:
                    if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                        print('User {} has no login profile'.format(user_report['user']))


if __name__ == '__main__':
    main(sys.argv[1:])
