#!/usr/bin/python
# This script simply gives a list of the current account IAM user
import boto3
import sys
import datetime,time
from time import sleep
import csv

def main(argv):

   MAX_PASSWORD_AGE=365

   iam_resource = boto3.resource('iam')
   iam_client = boto3.client('iam')

   credential_report = get_credential_report(iam_client)

   for row in credential_report:
     if row['password_enabled'] == "true":
       password_age = number_of_days_since_now(row['password_last_changed'])
       if password_age > MAX_PASSWORD_AGE:
         print ("%s;%s" % (row['user'],password_age))

def get_credential_report(iam_client):
    resp = iam_client.generate_credential_report()
    if resp['State'] == 'COMPLETE' :
        try: 
            response = iam_client.get_credential_report()
            credential_report_csv = response['Content']
            reader = csv.DictReader(credential_report_csv.splitlines())
            # print(reader.fieldnames)
            credential_report = []
            for row in reader:
                credential_report.append(row)
            return(credential_report)
        except ClientError as e:
            print("Unknown error getting Report: " + e.message)
    else:
        sleep(2)
        return get_credential_report(iam_client)

def number_of_days_since_now(mydate):

  if mydate :
     now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

     mydate_dec = time.mktime(datetime.datetime.strptime(mydate, "%Y-%m-%dT%H:%M:%S+00:00").timetuple())
     now_dec = time.mktime(datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S").timetuple())

     active_days = (now_dec - mydate_dec)/60/60/24
     return int(round(active_days))
  else:
    return -1

if __name__ == '__main__':
    main(sys.argv[1:])

