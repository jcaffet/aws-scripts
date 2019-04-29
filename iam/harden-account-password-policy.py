#!/usr/bin/python
# This script hardens if necessary the account password policy
# Pay attention that credential reports are renewed by AWS every 4 hours.
import boto3
from botocore.exceptions import ClientError
import sys

def main(argv):

    REQUIRE_UPPERCASE_CHARACTERS = True
    REQUIRE_LOWERCASE_CHARACTERS = True
    ALLOW_USERS_TO_CHANGE_PASSWORD = True
    REQUIRE_SYMBOLS = True
    REQUIRE_NUMBERS = True
    MINIMUM_PASSWORD_LENGTH = 9
    PASSWORD_REUSE_PREVENTION = 24
    MAX_PASSWORD_AGE = 90
    HARD_EXPIRY = False
    
    updatePolicyRequired = False
    iam_client = boto3.client('iam')
    try:
        password_policy = iam_client.get_account_password_policy()
        if password_policy['PasswordPolicy']['RequireUppercaseCharacters'] != REQUIRE_UPPERCASE_CHARACTERS:
            print("IAM password policy does not require at least one uppercase letter")
            updatePolicyRequired = True
        if password_policy['PasswordPolicy']['RequireLowercaseCharacters'] != REQUIRE_LOWERCASE_CHARACTERS:
            print("IAM password policy does not require at least one lowercase letter.")
            updatePolicyRequired = True
        if password_policy['PasswordPolicy']['AllowUsersToChangePassword'] != ALLOW_USERS_TO_CHANGE_PASSWORD:
            print("IAM password policy does not allow users to change his password.")
            updatePolicyRequired = True
        if password_policy['PasswordPolicy']['RequireSymbols'] != REQUIRE_SYMBOLS:
            print("IAM password policy does not require at least one symbol.")
            updatePolicyRequired = True
        if password_policy['PasswordPolicy']['RequireNumbers'] != REQUIRE_NUMBERS:
            print("IAM password policy does not require at least one number.")
            updatePolicyRequired = True
        if password_policy['PasswordPolicy']['MinimumPasswordLength'] < MINIMUM_PASSWORD_LENGTH:
            print("IAM password policy does not require minimum password length of %s or greater." % (MINIMUM_PASSWORD_LENGTH))
            updatePolicyRequired = True
        if 'PasswordReusePrevention' not in password_policy['PasswordPolicy'].keys() or \
            password_policy['PasswordPolicy']['PasswordReusePrevention'] < PASSWORD_REUSE_PREVENTION:
            print("IAM password policy does not prevent password reuse or duration is lower than %s." % (PASSWORD_REUSE_PREVENTION))
            updatePolicyRequired = True
        if 'MaxPasswordAge' not in password_policy['PasswordPolicy'].keys() or \
            password_policy['PasswordPolicy']['MaxPasswordAge'] < MAX_PASSWORD_AGE:
            print("IAM password policy does not expire passwords within %s days or less." % (MAX_PASSWORD_AGE))
            updatePolicyRequired = True
    except ClientError as e:
        if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
            print('There is no Password Policy for this account.')
            updatePolicyRequired = True

    if updatePolicyRequired:
        try:
            iam_client.update_account_password_policy(RequireUppercaseCharacters = REQUIRE_UPPERCASE_CHARACTERS,
                                                      RequireLowercaseCharacters = REQUIRE_LOWERCASE_CHARACTERS,
                                                      AllowUsersToChangePassword = ALLOW_USERS_TO_CHANGE_PASSWORD,
                                                      RequireSymbols = REQUIRE_SYMBOLS,
                                                      RequireNumbers = REQUIRE_NUMBERS,
                                                      MinimumPasswordLength = MINIMUM_PASSWORD_LENGTH,
                                                      PasswordReusePrevention = PASSWORD_REUSE_PREVENTION,
                                                      MaxPasswordAge = MAX_PASSWORD_AGE,
                                                      HardExpiry = HARD_EXPIRY)
            print("Account Password Policy updated !")
        except ClientError as e:
            print("Unexpected error: {}" .format(e))
    else:
        print("The Password Policy is compliant, nothing to do")


if __name__ == '__main__':
    main(sys.argv[1:])
