# iam_access_key_rotation-secretmanager

This is a Python function made for AWS Lambda.

This function basically rotates a Secret like this:

![image](https://user-images.githubusercontent.com/103848038/221819488-954358b8-0b3b-4ff7-8749-da4173c720ed.png)

Why should I rotate it? Security reasons: No matter how sensitive your data is, credentials are always recommended to rotate. 

It will rotate your IAM Access Keys and renew your secret. You will be ISO 27001 (and many normatives) compliant.


First, you need to create the Secret manually (just once), then you need to have enviroment variables into your Lambda:


For this case my env. variable is:

Key: sec

Value: testrotation


This is because I have only one secret. You can have multiple secrets separate by ;

Example: Value: testrotation;testrotation2;testrotation3

The sectet value (In Secret Manager), must be composed with 3 Secret Keys:

UserName - AccessKeyId - SecretAccessKey

For the UserName secret Value you Must coincide with the IAM user you want to rotate access keys.

Secret (In secret Manager) must be created first in order to start using this Lambda.

You can schedule Lambda as you wish, (I prefer as a great practice, to do it daily) in most companies rotation must be acommplished every 90 days.

-------------

Code explanation: 

This is suitable for all the Access Key scenarios (This is because some admins can manually touch access keys from the console, this will manage every scenario, trying to eliminate every manual error)

2 active access keys : It will deactivate the oldest, delete the oldest, create a new AK, replace Secret and deactivate the remaining active. (Leaving active only the new one).

2 inactive access keys: It will delete both, and create a new one, updating secret.

1 active: and 1 inactive: It will rotate properly

1 inactive: and 1 active: It will rotate properly

1 active: it will create a new one, update secret and deactivate the "old" active"

1 inactive: it will delete it, create a new one, update secret

none: It will create 1, update secret
