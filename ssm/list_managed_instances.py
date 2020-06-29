'''
This script simply gives a list of the current Online SSM managed instances
'''
import sys
import boto3


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
    for instance_information in response['InstanceInformationList']:
        print("%s;%s;%s;%s" % (instance_information['InstanceId'],
                               instance_information['PingStatus'],
                               instance_information['AgentVersion'],
                               instance_information['PlatformName']))


if __name__ == '__main__':
    main(sys.argv[1:])
