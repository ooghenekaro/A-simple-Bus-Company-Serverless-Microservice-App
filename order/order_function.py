import boto3
import uuid

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    orders_table = dynamodb.Table('Orders')
    headers = {
        "Access-Control-Allow-Origin": "*",  # Allows all origins
        "Access-Control-Allow-Credentials": "true",  # Allows credentials (cookies, headers, etc.)
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",  # Allows these headers
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"  # Allows these HTTP methods
    }    
    order_id = str(uuid.uuid4())
    orders_table.put_item(Item={'order_id': order_id, **event})
    
    return {
        'statusCode': 200,
        'body': f'Order placed successfully with ID {order_id}'
    }
