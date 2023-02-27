import json
import boto3
import os
import datetime
from datetime import date

iam = boto3.client('iam')
secretsmanager = boto3.client('secretsmanager')

def lambda_handler(event, context):   
    vsecret = os.getenv('sec')
    secret_list = vsecret.split(';')

    for secret in secret_list:
        get_secret = secretsmanager.get_secret_value(SecretId=secret)
        secret_details = json.loads(get_secret['SecretString'])
        
        # Extracting the key details from IAM
        key_response = iam.list_access_keys(UserName=secret_details['UserName'])
        cont = 0
        # Existing Key Inactivation
        for key in key_response['AccessKeyMetadata']:
            cont = cont + 1

        if cont == 2:
     
            for secret in secret_list:
                get_secret = secretsmanager.get_secret_value(SecretId=secret)
                secret_details = json.loads(get_secret['SecretString'])
                
                print("For user - " + secret_details['UserName'] + ", Oldest Access Key will be inactivated.")

                # Extracting the key details from IAM
                key_response = iam.list_access_keys(UserName=secret_details['UserName'])
                key_date = key_response['AccessKeyMetadata'][1]['CreateDate']
                key_date = key_date.strftime("%Y-%m-%d %H:%M:%S")

                # Existing Key Inactivation
                for key in key_response['AccessKeyMetadata']:
                    key_comp = key['CreateDate']
                    key_comp = key_comp.strftime("%Y-%m-%d %H:%M:%S")
                    if key_date > key_comp:
                        iam.update_access_key(AccessKeyId=key['AccessKeyId'], Status='Inactive',UserName=key['UserName'])
                        print(key['AccessKeyId'] + " key of " + key['UserName'] + " has been inactivated.")

    for secret in secret_list:
        get_secret = secretsmanager.get_secret_value(SecretId=secret)
        secret_details = json.loads(get_secret['SecretString'])

        print("For user - " + secret_details['UserName'] + ", inactive Access & Secret keys will be deleted.")
        
        # Extracting the key details from IAM
        key_response = iam.list_access_keys(UserName=secret_details['UserName'])
        
        # Inactive Key Deletion
        for key in key_response['AccessKeyMetadata']:
            if key['Status'] == 'Inactive':
                iam.delete_access_key(AccessKeyId=key['AccessKeyId'],UserName=key['UserName'])
                print("An inactive key - " + key['AccessKeyId'] + ", of " + key['UserName'] + " user has been deleted.")

    for secret in secret_list:
        get_secret = secretsmanager.get_secret_value(SecretId=secret)
        secret_details = json.loads(get_secret['SecretString'])
        
        # Extracting the key details from IAM
        key_response = iam.list_access_keys(UserName=secret_details['UserName'])

        # New Key Creation
        create_response = iam.create_access_key(UserName=secret_details['UserName'])
        print("A new set of keys has been created for user - " + secret_details['UserName'])
        
        # Updating the secret value
        NewSecret = '{"UserName":"' + create_response['AccessKey']['UserName'] + '", "AccessKeyId":"' + create_response['AccessKey']['AccessKeyId'] + '", "SecretAccessKey":"' + create_response['AccessKey']['SecretAccessKey'] + '"}'
        secretsmanager.update_secret(SecretId=secret,SecretString=NewSecret)
        print(secret + " secret has been updated with latest key details for " + secret_details['UserName'] + " user.")

    for secret in secret_list:
        get_secret = secretsmanager.get_secret_value(SecretId=secret)
        secret_details = json.loads(get_secret['SecretString'])
        
        # Extracting the key details from IAM
        key_response = iam.list_access_keys(UserName=secret_details['UserName'])
        cont2 = 0
        # Existing Key Inactivation
        for key in key_response['AccessKeyMetadata']:
            cont2 = cont2 + 1

            if cont2 == 2:

                key_date = key_response['AccessKeyMetadata'][1]['CreateDate']
                key_date = key_date.strftime("%Y-%m-%d %H:%M:%S")

                # Existing Key Inactivation
                for key in key_response['AccessKeyMetadata']:
                    key_comp = key['CreateDate']
                    key_comp = key_comp.strftime("%Y-%m-%d %H:%M:%S")
                    if key_date > key_comp:
                        iam.update_access_key(AccessKeyId=key['AccessKeyId'], Status='Inactive',UserName=key['UserName'])
                        print(key['AccessKeyId'] + " key of " + key['UserName'] + " has been inactivated.")

    return "Process of deletion of inactive keys, key creation & secret update has completed successfully."