'''
This script simply gives a CSV ist of the current account IAM users
'''
import boto3


def main():
    '''
    Simply connects to AWS API with boto3 and prints the result
    '''
    iam = boto3.resource('iam')
    users = iam.users.all()
    print("user_name;create_date;password_last_used")
    for user in users:
        print("%s;%s;%s" % (user.user_name,
                            user.create_date,
                            user.password_last_used))


if __name__ == '__main__':
    main()
