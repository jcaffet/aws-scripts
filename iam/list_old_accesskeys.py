'''
Pay attention that credential reports are renewed by AWS every 4 hours.
'''
import sys
import boto3
import utils


def main(argv):

    max_accesskey_age = 180

    iam_client = boto3.client('iam')
    awsaccountid = boto3.client('sts').get_caller_identity()['Account']
    credential_report = utils.get_credential_report(iam_client)
    print("account_id;accesskeyid;max_accesskey_age;username;accesskey_create_date;accesskey_create_age")
    for user_report in credential_report:
        iamuser = user_report['user']
        if iamuser != "<root_account>":
            list_not_rotated_accesskeys(iam_client, iamuser, max_accesskey_age, awsaccountid)


def list_not_rotated_accesskeys(iam_client, iamuser, max_accesskey_age, my_account):
    response = iam_client.list_access_keys(UserName=iamuser)
    for accesskey in response['AccessKeyMetadata']:
        accesskey_create_date = accesskey['CreateDate']
        accesskey_create_age = utils.number_of_days_since_now_datetime(accesskey_create_date)
        if accesskey_create_age > max_accesskey_age:
            print("%s;%s;%s;%s;%s;%s" % (my_account,
                                         accesskey['AccessKeyId'],
                                         max_accesskey_age,
                                         iamuser,
                                         accesskey_create_age,
                                         accesskey_create_date))


if __name__ == '__main__':
    main(sys.argv[1:])
