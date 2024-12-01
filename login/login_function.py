#import boto3

#def lambda_handler(event, context):
#    dynamodb = boto3.resource('dynamodb')
#    users_table = dynamodb.Table('Users')
#    headers = {
#        "Access-Control-Allow-Origin": "*",  # Allows all origins
#        "Access-Control-Allow-Credentials": "true",  # Allows credentials (cookies, headers, etc.)
#        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",  # Allows these headers
#        "Access-Control-Allow-Methods": "OPTIONS,POST,GET, PUT, DELETE"  # Allows these HTTP methods
#    }    
#    response = users_table.get_item(Key={'email': event['email']})
#    user = response.get('Item')
#    if user and user['password'] == event['password']:
#        return {
#            'statusCode': 200,
#            'headers': headers,
#            'body': json.dumps(f'Login successful, User ID: {user["user_id"]}')
#        }
#    return {
#        'statusCode': 401,
#        'body': 'Login failed'
#    }


import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    users_table = dynamodb.Table('Users')

    headers = {
        "Access-Control-Allow-Origin": "http://karo-static-new.s3-website.eu-west-2.amazonaws.com",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE"
    }

    # Parse the incoming request body
    if isinstance(event.get('body'), str):
        body = json.loads(event['body'])
    else:
        body = event.get('body', {})

    # Get user from DynamoDB
    response = users_table.get_item(Key={'email': body['email']})
    user = response.get('Item')

    if user and user['password'] == body['password']:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Login successful',
                'user_id': user['user_id']
            })
        }

    return {
        'statusCode': 401,
        'headers': headers,
        'body': json.dumps({
            'message': 'Login failed'
        })
    }
