#!/usr/bin/python
# This script simply checks and activates default EBS encryption
# Scope : per account and per region
import boto3
import boto3.ec2
import sys

def main(argv):
    AwsAccountId = boto3.client('sts').get_caller_identity()['Account']
    RegionName = boto3.session.Session().region_name
    ec2_client = boto3.client('ec2')
    try:
        is_ebs_encrypted_by_default = ec2_client.get_ebs_encryption_by_default()['EbsEncryptionByDefault']
        if is_ebs_encrypted_by_default:
            print("EbsEncryptionByDefault is already activated")
        else:
            print("EbsEncryptionByDefault is not already activated, let's activate it.")
            response = ec2_client.enable_ebs_encryption_by_default()
            print("EbsEncryptionByDefault for %s on %s is now : %s" % (AwsAccountId,
                                                                       RegionName,
                                                                       response['EbsEncryptionByDefault']))
    except ClientError as e:
        print(e)


if __name__ == '__main__':
    main(sys.argv[1:])
