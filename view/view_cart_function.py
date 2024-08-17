import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    carts_table = dynamodb.Table('Carts')
    headers = {
        "Access-Control-Allow-Origin": "*",  # Allows all origins
        "Access-Control-Allow-Credentials": "true",  # Allows credentials (cookies, headers, etc.)
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",  # Allows these headers
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET, PUT, DELETE"  # Allows these HTTP methods
    }    
    user_id = event['user_id']
    response = carts_table.query(KeyConditionExpression=Key('user_id').eq(user_id))
    
    return {
        'statusCode': 200,
        'body': response.get('Items', [])
    }
