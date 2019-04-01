#!/usr/bin/python
# This script gives the list of the RDS databases with some additional information

import boto3
import sys


def main(argv):
    client = boto3.client('rds')
    response = client.describe_db_instances()
    instances = response.get('DBInstances')

    for instance in instances:
        db_identifier = instance.get('DBInstanceIdentifier')
        db_instanceclass = instance.get('DBInstanceClass')
        db_status = instance.get('DBInstanceStatus')

        print("%s;%s;%s" % (db_identifier, db_instanceclass, db_status))

if __name__ == '__main__':
    main(sys.argv[1:])

