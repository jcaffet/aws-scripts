'''
this script gives the list of the current account Auto Scaling Groups (ASG)
depending on one key/value tag
The script uses JMESPath as query language as query language
'''
import sys
import boto3


def main(argv):

    TAG_KEY = 'someKey'
    TAG_VALUE = 'someValue'

    client = boto3.client('autoscaling')
    paginator = client.get_paginator('describe_auto_scaling_groups')
    page_iterator = paginator.paginate(
        PaginationConfig={'PageSize': 100}
    )

    filtered_asgs = page_iterator.search(
        'AutoScalingGroups[] | [?contains(Tags[?Key==`{}`].Value, `{}`)]'.format(TAG_KEY,TAG_VALUE))

    for asg in filtered_asgs:
        print(asg['AutoScalingGroupName'])


if __name__ == '__main__':
    main(sys.argv[1:])
