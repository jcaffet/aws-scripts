#!/usr/bin/python
# This script displays the list of the EC2 instances for which it is not possible to load their AMI.
# Maybe because the AMI has been deregisted or permissions have changed
# This will cause major unpleasant effects for any change on the EC2 lifecycle.
# This script lists all ec2 instances of an account and a region : id;name;stack_name;image_id
import boto3
import boto3.ec2
import sys

def main(argv):
    
    ec2 = boto3.resource('ec2')

    allInstances = ec2.instances.all()
    allInstanceAmiIds=list([instance.image_id for instance in allInstances])

    # check first if allInstanceAmiIds is empty otherwise ec2.images.filter will retreive all image and take long time
    if allInstanceAmiIds:
        # the following filter will only return AMI information of the visible AMI in parameter and will forget the others
        allInstanceUniqueAmiIds = list(set(allInstanceAmiIds))
        visibleInstanceAmis = ec2.images.filter(ImageIds=allInstanceUniqueAmiIds)
        visibleInstanceAmiIds = list([image.image_id for image in visibleInstanceAmis])
        for instance in allInstances:
            if instance.image_id not in visibleInstanceAmiIds:
                print("%s;%s;%s" % (instance.instance_id, instance.image_id, getInstanceName(instance)))

def getInstanceName(ec2_instance):
    instance_name=''
    if ec2_instance.tags:
        for tag in ec2_instance.tags:
            if tag["Key"] == 'Name':
                instance_name = tag["Value"]
    return instance_name


if __name__ == '__main__':
    main(sys.argv[1:])

