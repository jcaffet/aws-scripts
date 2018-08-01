#!/usr/bin/python
# This script displays the list of the EC2 instances for which it is not possible to load details.
# Maybe because the AMI has been deregisted or permissions have changed
# This will cause major unpleasant effects for any change on the EC2 lifecycle.

import boto3
import boto3.ec2
import sys

# This script lists all ec2 instances of an account : id;name;stack_name;image_id

def main(argv):
    ec2 = boto3.resource('ec2')
    
    instances = ec2.instances.all()
    instance_ami_ids=list([instance.image_id for instance in instances])

    visible_images = ec2.images.filter(ImageIds=instance_ami_ids)
    visible_image_ids=list([image.image_id for image in visible_images])

    for instance in instances:
       if instance.image_id not in visible_image_ids:
          print("%s;%s;%s" % (instance.instance_id,instance.image_id,get_instance_name(instance)))


def get_instance_name(ec2_instance):
    instance_name=''
    if ec2_instance.tags:
        for tag in ec2_instance.tags:
            if tag["Key"] == 'Name':
                instance_name = tag["Value"]
    return instance_name


if __name__ == '__main__':
    main(sys.argv[1:])

