import boto3
import uuid

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    bookings_table = dynamodb.Table('Bookings')
    headers = {
        "Access-Control-Allow-Origin": "*",  # Allows all origins
        "Access-Control-Allow-Credentials": "true",  # Allows credentials (cookies, headers, etc.)
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",  # Allows these headers
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"  # Allows these HTTP methods
    }    
    booking_id = str(uuid.uuid4())
    bookings_table.put_item(Item={'booking_id': booking_id, **event})
    
    return {
        'statusCode': 200,
        'body': f'Booking successful with ID {booking_id}'
    }
