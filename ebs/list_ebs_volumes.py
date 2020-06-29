'''
This script simply gives a csv list of the current account and region EC2 EBS
'''
import boto3
import boto3.ec2


def main():
    '''
    Simply connects to AWS API with boto3 and prints the result
    '''
    awsaccountid = boto3.client('sts').get_caller_identity()['Account']
    awsregion = boto3.session.Session().region_name
    ec2 = boto3.resource('ec2')
    volumes = ec2.volumes.all()
    print("awsaccountid;awsregion;id;size;type;state;encrypted")
    for volume in volumes:
        print("%s;%s;%s;%s;%s;%s;%s" % (awsaccountid,
                                        awsregion,
                                        volume.id,
                                        volume.size,
                                        volume.volume_type,
                                        volume.state,
                                        volume.encrypted))


if __name__ == '__main__':
    main()
