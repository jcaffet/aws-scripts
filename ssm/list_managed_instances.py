#!/usr/bin/python
# This script simply gives a list of the current Online SSM managed instances
import boto3
import sys


def main(argv):

    ssm_client = boto3.client('ssm')
    response = ssm_client.describe_instance_information(
            Filters=[
        {
            'Key': 'PingStatus',
            'Values': [
                'Online',
            ]
        },
    ],
    )
    print(response['InstanceInformationList'])


if __name__ == '__main__':
    main(sys.argv[1:])

