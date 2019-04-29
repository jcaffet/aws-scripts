#!/usr/bin/python
# This script simply gives a list of the current account EC2 instance with some additionnal details
import boto3
import boto3.ec2
import sys


def main(argv):
    AwsAccountId = boto3.client('sts').get_caller_identity()['Account']
    RegionName = boto3.session.Session().region_name
    ec2 = boto3.resource('ec2')
    volumes = ec2.volumes.all()
    volumes = ec2.volumes.filter(Filters=[{'Name': 'volume-type', 'Values': ['standard']}])
    for volume in volumes:
        print("%s;%s;%s;%s" % (AwsAccountId, RegionName,volume.id, volume.state))


if __name__ == '__main__':
    main(sys.argv[1:])

