# iam_access_key_rotation-secretmanager

This is an AWS Lambda python function made for AWS Lambda.

Process will be like this:

![grafico Rotate222_ok](https://user-images.githubusercontent.com/103848038/221845183-9e005726-362d-48b6-9723-522d4fa17da1.png)

Note that your applications will retrieve a secrete from secret manager, based on the Access/Secret Keys from the first column. You will never have "downtime" of your applications.

Why should I rotate my access/security keys? Security reasons: No matter how sensitive your data is, credentials are always recommended to rotate. 

This function basically rotates a Secret like this:

![image](https://user-images.githubusercontent.com/103848038/221819488-954358b8-0b3b-4ff7-8749-da4173c720ed.png)

I know putting a Secret Key here could make you a bit uncomfortable, but what if you rotate it a lot? And what if you retrieve secret only from your known sources?


Function will rotate your IAM Access Keys and renew your secret. You will be ISO 27001 (and many normatives) compliant.


First, you need to create the Secret manually (just once), then you need to have enviroment variables into your Lambda:


For this case my env. variable is:

>**Key: sec**

>**Value: testrotation**


This is because I have only one secret. You can have multiple secrets separate by ;

Example: Value: testrotation;testrotation2;testrotation3

The sectet value (In Secret Manager), must be composed with 3 Secret Keys:

>**UserName - AccessKeyId - SecretAccessKey**

For the UserName secret Value you Must coincide with the IAM user you want to rotate access keys.

As I said before, secret (In secret Manager) must be created first in order to start using this Lambda.

You can schedule Lambda as you wish, (I prefer as a nice best practice, to do it daily) in most companies rotation must be acommplished every 90 days. Trigger your function with Eventbridge schedule rule.


-------------


**Role:** 

Attach the Role LambdaExecutionRole.json to the execution Role in your Lambda function.


-------------


**Code considerations and logic:** 

This is suitable for all the Access Key scenarios (This is because some admins can manually touch access keys from the console. Function will manage every scenario and will try to eliminate manual errors)

![image](https://user-images.githubusercontent.com/103848038/221890296-0e02bfe5-3da5-4650-9a7c-0d850c4d637b.png)

e.g.:


If 2 access keys are active: It will deactivate the different ones from the Secret Manager, next it will delete the inactive, create a new AK, replace Secret and deactivate the remaining active. (Leaving active only the new one).

If you have 2 inactive access keys: It will delete both, and create a new one, updating secret.

If you have 1 active: and 1 inactive: It will delete inactive, activate a new one, update secret with new one and inactive remaining.

If you have 1 active: it will create a new one, update secret and deactivate the "old" active"

If you have 1 inactive: it will delete it, create a new one, update secret

If you have none: It will create 1, update secret


-------------

**A personal advice:** 

Increase Security by limiting sources from where you can retrieve Secret. Take a look of the examples here: https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html


