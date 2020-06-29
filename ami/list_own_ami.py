'''
This script lists all the AMIs of your own account with some additional details
'''
import sys
import boto3
import boto3.ec2


def main(argv):

    ec2 = boto3.resource('ec2')
    images = ec2.images.filter(Owners=['self'])

    for image in images:
        print("%s;%s;%s:%s" % (image.image_id,
                               image.owner_id,
                               image.name,
                               image.description))


if __name__ == '__main__':
    main(sys.argv[1:])
