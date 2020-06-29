'''
This script simply gives the list of the current account Auto Scaling Groups

'''
import sys
import boto3
import boto3.ec2


def main(argv):

    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups()
    list_items = response.get('AutoScalingGroups')

    while 'LastEvaluatedKey' in response:
        response = client.describe_auto_scaling_groups(ExclusiveStartKey=response['LastEvaluatedKey'])
        list_items.extend(response.get('AutoScalingGroups'))

    for asg in list_items:
        print("%s" % (asg.get('AutoScalingGroupName')))


if __name__ == '__main__':
    main(sys.argv[1:])
