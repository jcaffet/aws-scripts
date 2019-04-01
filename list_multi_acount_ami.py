#!/usr/bin/python

import boto3
import boto3.ec2
import sys

# This script lists all ec2 instances of an account : id;name;stack_name;image_id

def main(argv):
    ec2 = boto3.resource('ec2')

    myAccounts = ['629307289374', '395174950964']
    images = ec2.images.filter(Owners=myAccounts)

    for image in images:
        print("%s;%s;%s:%s" % (image.image_id,image.owner_id,image.name,image.description))

if __name__ == '__main__':
    main(sys.argv[1:])
