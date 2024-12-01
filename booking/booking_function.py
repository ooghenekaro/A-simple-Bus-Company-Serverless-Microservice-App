#import boto3
#import uuid

#def lambda_handler(event, context):
#    dynamodb = boto3.resource('dynamodb')
#    bookings_table = dynamodb.Table('Bookings')

#    headers = {
#        "Access-Control-Allow-Origin": "http://karo-static-new.s3-website.eu-west-2.amazonaws.com",
#        "Access-Control-Allow-Credentials": "true",
#        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
#        "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE"
#    }

#    booking_id = str(uuid.uuid4())
#    bookings_table.put_item(Item={'booking_id': booking_id, **event})

#    return {
#        'statusCode': 200,
#        'headers': headers,
#        'body': json.dumps(f'Booking successful with ID {booking_id}')
#    }


import boto3
import uuid
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    bookings_table = dynamodb.Table('Bookings')

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

    # Generate booking ID
    booking_id = str(uuid.uuid4())
    
    # Create the item to store
    booking_item = {
        'booking_id': booking_id,
        'user_id': body.get('user_id'),
        'trip_id': body.get('trip_id'),
        'seats': body.get('seats')
    }

    # Store in DynamoDB
    bookings_table.put_item(Item=booking_item)

    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'message': f'Booking successful with ID {booking_id}',
            'booking_id': booking_id
        })
    }
