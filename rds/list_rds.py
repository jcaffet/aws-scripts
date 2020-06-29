'''
This script gives the CSV list of the RDS databases
'''
import boto3


def main():
    '''
    Simply connects to AWS API with boto3 and prints the result
    '''
    client = boto3.client('rds')
    response = client.describe_db_instances()
    instances = response.get('DBInstances')

    print("DBInstanceIdentifier;DBInstanceClass;DBInstanceStatus;PubliclyAccessible;StorageEncrypted")
    for instance in instances:
        print("%s;%s;%s;%s;%s" % (instance.get('DBInstanceIdentifier'),
                                 instance.get('DBInstanceClass'),
                                 instance.get('DBInstanceStatus'),
                                 instance.get('PubliclyAccessible'),
                                 instance.get('StorageEncrypted')))


if __name__ == '__main__':
    main()
