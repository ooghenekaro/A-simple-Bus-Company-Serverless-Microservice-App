#import boto3

#def lambda_handler(event, context):
#    dynamodb = boto3.resource('dynamodb')
#    carts_table = dynamodb.Table('Carts')
#    headers = {
#        "Access-Control-Allow-Origin": "*",  # Allows all origins
#        "Access-Control-Allow-Credentials": "true",  # Allows credentials (cookies, headers, etc.)
#        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",  # Allows these headers
#        "Access-Control-Allow-Methods": "OPTIONS,POST,GET, PUT, DELETE"  # Allows these HTTP methods
#    }    
#    user_id = event['user_id']
#    response = carts_table.query(KeyConditionExpression=Key('user_id').eq(user_id))
    
#    return {
#        'statusCode': 200,
#        'headers': headers,
#        'body': response.get('Items', [])
#    }



import boto3
from boto3.dynamodb.conditions import Key
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    carts_table = dynamodb.Table('Carts')

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

    user_id = body.get('user_id')
    
    # Query cart items for the user
    response = carts_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )

    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'cart_items': response.get('Items', [])
        })
    }
