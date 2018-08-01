#!/usr/bin/python
# This script simply gives a list of the current account IAM users (with some details)
import boto3
import sys

def main(argv):

   iam = boto3.resource('iam')
   users = iam.users.all()
   print("user_name;user_create_date;user_password_last_used")
   for user in users:
      print("%s;%s;%s" % (user.user_name, user.create_date, user.password_last_used))


if __name__ == '__main__':
    main(sys.argv[1:])

