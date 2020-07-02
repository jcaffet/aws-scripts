'''
This script displays a list of unsed IAM users
They match the folling conditions :
 - user is older than max_activity_age
 - no password access older than max_activity_age
 - no accesskey usage older than max_activity_age
'''
import sys
import boto3
import utils


def main(argv):

    max_activity_age = 90

    iam_client = boto3.client('iam')
    iam_resource = boto3.resource('iam')
    all_users = iam_resource.users.all()

    print("user_name;user_age;last_password_login_age;most_recent_accesskey_usage_age")
    for user in all_users:
        most_recent_accesskey_usage_age = get_older_accesskey_usage_age(iam_client, user)
        user_age = utils.number_of_days_since_now_datetime(user.create_date)
        last_password_login_age = utils.number_of_days_since_now_datetime(user.password_last_used)

        if (last_password_login_age > max_activity_age or last_password_login_age == -1) \
            and (most_recent_accesskey_usage_age > max_activity_age or most_recent_accesskey_usage_age == -1) \
            and (user_age > max_activity_age):
            print("%s;%s;%s;%s" % (user.user_name, user_age, last_password_login_age, most_recent_accesskey_usage_age))


def get_older_accesskey_usage_age(iam_client, user):

    recent_accesskey_age = -1
    for key in user.access_keys.all():
        last_used_key = iam_client.get_access_key_last_used(AccessKeyId=key.id)
        if 'LastUsedDate' in last_used_key['AccessKeyLastUsed']:
            accesskeydate = last_used_key['AccessKeyLastUsed']['LastUsedDate']
            accesskey_age = utils.number_of_days_since_now_datetime(accesskeydate)
            if recent_accesskey_age == -1:
                recent_accesskey_age = accesskey_age
            else:
                recent_accesskey_age = min(accesskey_age, recent_accesskey_age)
    return recent_accesskey_age


if __name__ == '__main__':
    main(sys.argv[1:])
