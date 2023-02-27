# iam_access_key_rotation-secretmanager

This is for AWS Lambda

It will rotate your access keys and renew you secret.
You need to have enviroment variables:

For this case the env. variable is:

Key: sec
Value: testrotation

This is because I have only one secret. You can have multiple secrets separate by ;

Example: Value: testrotation;testrotation2;testrotation3

The sectet value (In Secret Manager), must be composed with 3 Secret Keys:

UserName
AccessKeyId
SecretAccessKey

For the UserName secret Value you Must coincide with the IAM user you want to rotate access keys.
