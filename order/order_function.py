#import boto3
#import uuid

#def lambda_handler(event, context):
#    dynamodb = boto3.resource('dynamodb')
#    orders_table = dynamodb.Table('Orders')
#    headers = {
#        "Access-Control-Allow-Origin": "*",  # Allows all origins
#        "Access-Control-Allow-Credentials": "true",  # Allows credentials (cookies, headers, etc.)
#        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",  # Allows these headers
#        "Access-Control-Allow-Methods": "OPTIONS,POST,GET, PUT, DELETE"  # Allows these HTTP methods
#    }    
#    order_id = str(uuid.uuid4())
#    orders_table.put_item(Item={'order_id': order_id, **event})
    
#    return {
#        'statusCode': 200,
#        'headers': headers,
#        'body': json.dumps(f'Order placed successfully with ID {order_id}')
#    }


import boto3
import uuid
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    orders_table = dynamodb.Table('Orders')

    headers = {
        "Access-Control-Allow-Origin": "http://karo-static-new.s3-website.eu-west-2.amazonaws.com",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE"
    }

    # Parse the body if it's a string
    if isinstance(event.get('body'), str):
        body = json.loads(event['body'])
    else:
        body = event.get('body', {})

    # Generate order ID
    order_id = str(uuid.uuid4())
    
    # Create the item to store
    order_item = {
        'order_id': order_id,
        'user_id': body.get('user_id'),
        'product_id': body.get('product_id'),
        'quantity': body.get('quantity')
    }

    # Store in DynamoDB
    orders_table.put_item(Item=order_item)

    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'message': f'Order placed successfully with ID {order_id}',
            'order_id': order_id
        })
    }
