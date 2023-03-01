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
        key_response = iam.list_access_keys(UserName=secret_details['UserName'])
        cont = 0
        for key in key_response['AccessKeyMetadata']:
            cont = cont + 1
        #This counter validates the 2 access key limit from AWS. It will only enter if there is two AK.
            if cont == 2:   
                for secret in secret_list:
                    get_secret = secretsmanager.get_secret_value(SecretId=secret)
                    secret_details = json.loads(get_secret['SecretString'])              
                    key_response = iam.list_access_keys(UserName=secret_details['UserName'])
                    status1 = key_response['AccessKeyMetadata'][0]['Status']
                    status2 = key_response['AccessKeyMetadata'][1]['Status']
                    akfromsecret = secret_details['AccessKeyId']

                    for key in key_response['AccessKeyMetadata']:
                        #If status of both AK are the same, it will inactivate the different from secret manager, to ensure is not in use.
                        if status1 == status2:
                            if akfromsecret != key['AccessKeyId']:
                                iam.update_access_key(AccessKeyId=key['AccessKeyId'], Status='Inactive',UserName=key['UserName'])
                                print(key['AccessKeyId'] + " INACTIVATED ")

    #This will delete the inactive AK.
    for secret in secret_list:
        get_secret = secretsmanager.get_secret_value(SecretId=secret)
        secret_details = json.loads(get_secret['SecretString'])        
        key_response = iam.list_access_keys(UserName=secret_details['UserName'])
        
        # Inactive Key will be deleted
        for key in key_response['AccessKeyMetadata']:
            if key['Status'] == 'Inactive':
                iam.delete_access_key(AccessKeyId=key['AccessKeyId'],UserName=key['UserName'])
                print(key['AccessKeyId'] + " DELETED")

    #This will create a new AK and update the Secret
    for secret in secret_list:
        get_secret = secretsmanager.get_secret_value(SecretId=secret)
        secret_details = json.loads(get_secret['SecretString'])        
        key_response = iam.list_access_keys(UserName=secret_details['UserName'])
        create_response = iam.create_access_key(UserName=secret_details['UserName'])
        
        NewSecret = '{"UserName":"' + create_response['AccessKey']['UserName'] + '", "AccessKeyId":"' + create_response['AccessKey']['AccessKeyId'] + '", "SecretAccessKey":"' + create_response['AccessKey']['SecretAccessKey'] + '"}'
        secretsmanager.update_secret(SecretId=secret,SecretString=NewSecret)
        print(secret + " UPDATED")

    #This will inactivate the oldest one, right after a new one was created and updated in Secret Manager.
    for secret in secret_list:
        get_secret = secretsmanager.get_secret_value(SecretId=secret)
        secret_details = json.loads(get_secret['SecretString'])
        key_response = iam.list_access_keys(UserName=secret_details['UserName'])
        cont2 = 0
        for key in key_response['AccessKeyMetadata']:
            cont2 = cont2 + 1
            if cont2 == 2:
                key_date = key_response['AccessKeyMetadata'][1]['CreateDate']
                key_date = key_date.strftime("%Y-%m-%d %H:%M:%S")
                for key in key_response['AccessKeyMetadata']:
                    key_comp = key['CreateDate']
                    key_comp = key_comp.strftime("%Y-%m-%d %H:%M:%S")
                    if key_date > key_comp:
                        iam.update_access_key(AccessKeyId=key['AccessKeyId'], Status='Inactive',UserName=key['UserName'])
                        print(key['AccessKeyId'] + " INACTIVATED")

    return "Process completed successfully."
