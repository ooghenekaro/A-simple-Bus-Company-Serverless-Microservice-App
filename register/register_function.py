import json
import boto3
import uuid

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    users_table = dynamodb.Table('Users')

    user_id = str(uuid.uuid4())
    users_table.put_item(Item={'user_id': user_id, **event})

    headers = {
        "Access-Control-Allow-Origin": "*",  # Allows all origins
        "Access-Control-Allow-Credentials": "true",  # Allows credentials (cookies, headers, etc.)
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",  # Allows these headers
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"  # Allows these HTTP methods
    }

    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({'message': f'User registered successfully with ID {user_id}'})
    }

