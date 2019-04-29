#!/usr/bin/python
# This script simply gives a list of the current account EC2 instance with some additionnal details
import boto3
import boto3.ec2
import sys


def main(argv):
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.all()
    for instance in instances:
        print("%s;%s;%s;%s;%s" % (instance.id, get_instance_name(instance),get_instance_stack_name(instance),get_instance_image_id(instance),get_instance_state(instance)))


def get_instance_name(ec2_instance):
    instance_name=''
    if ec2_instance.tags:
        for tag in ec2_instance.tags:
            if tag["Key"] == 'Name':
                instance_name = tag["Value"]
    return instance_name

def get_instance_stack_name(ec2_instance):
    stack_name = ''
    if ec2_instance.tags:
        for tags in ec2_instance.tags:
            if tags["Key"] == 'aws:cloudformation:stack-name':
                stack_name = tags["Value"]
    return stack_name

def get_instance_image_id(ec2_instance):
    return ec2_instance.image_id

def get_instance_state(ec2_instance):
    return ec2_instance.state['Name']

if __name__ == '__main__':
    main(sys.argv[1:])

