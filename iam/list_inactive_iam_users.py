#!/usr/bin/python
# This script displays a list of unsed IAM users
# They match the folling conditions :
# - user is older than MAX_ACTIVITY_AGE
# - no password access older than MAX_ACTIVITY_AGE
# - no accesskey usage older than MAX_ACTIVITY_AGE
import boto3
import sys
import datetime,time

def main(argv):

  MAX_ACTIVITY_AGE=365

  iam_client = boto3.client('iam')
  iam_resource = boto3.resource('iam')
  all_users = iam_resource.users.all()

  for user in all_users:
    most_recent_accesskey_usage_age = get_older_accesskey_usage_age(iam_client, user)
    user_age = number_of_days_since_now(user.create_date)
    last_password_login_age = number_of_days_since_now(user.password_last_used)

    if  (last_password_login_age > MAX_ACTIVITY_AGE or last_password_login_age == -1) \
        and (most_recent_accesskey_usage_age > MAX_ACTIVITY_AGE or most_recent_accesskey_usage_age == -1) \
        and (user_age > MAX_ACTIVITY_AGE):
      print("%s;%s;%s;%s" % (user.user_name, user_age, last_password_login_age, most_recent_accesskey_usage_age))


def get_older_accesskey_usage_age(iam_client, user):

  recent_accesskey_age = -1
  for key in user.access_keys.all():
    last_used_key = iam_client.get_access_key_last_used(AccessKeyId=key.id)
    if 'LastUsedDate' in last_used_key['AccessKeyLastUsed']:
      accesskeydate = last_used_key['AccessKeyLastUsed']['LastUsedDate']
      accesskey_age = number_of_days_since_now(accesskeydate)
      if recent_accesskey_age == -1 :
        recent_accesskey_age = accesskey_age
      else:
        recent_accesskey_age = min(accesskey_age , recent_accesskey_age)
  return recent_accesskey_age


def number_of_days_since_now(mydate):

  if mydate :
     mydate = mydate.strftime("%Y-%m-%d %H:%M:%S")
     now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

     mydate_dec = time.mktime(datetime.datetime.strptime(mydate, "%Y-%m-%d %H:%M:%S").timetuple())
     now_dec = time.mktime(datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S").timetuple())

     active_days = (now_dec - mydate_dec)/60/60/24
     return int(round(active_days))
  else:
    return -1


if __name__ == '__main__':
    main(sys.argv[1:])

