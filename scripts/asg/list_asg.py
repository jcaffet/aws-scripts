#!/usr/bin/python
# This script simply gives the list of the current account Auto Scaling Groups (ASG)
import boto3
import boto3.ec2
import sys


def main(argv):

   client = boto3.client('autoscaling')
   response = client.describe_auto_scaling_groups(MaxRecords=100)
   as_groups = response.get('AutoScalingGroups')

   for asg in as_groups:
      print("%s" % (asg.get('AutoScalingGroupName')))


if __name__ == '__main__':
    main(sys.argv[1:])

