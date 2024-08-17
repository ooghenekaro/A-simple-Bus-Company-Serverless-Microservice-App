import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    users_table = dynamodb.Table('Users')
    headers = {
        "Access-Control-Allow-Origin": "*",  # Allows all origins
        "Access-Control-Allow-Credentials": "true",  # Allows credentials (cookies, headers, etc.)
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",  # Allows these headers
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"  # Allows these HTTP methods
    }    
    response = users_table.get_item(Key={'email': event['email']})
    user = response.get('Item')
    if user and user['password'] == event['password']:
        return {
            'statusCode': 200,
            'body': f'Login successful, User ID: {user["user_id"]}'
        }
    return {
        'statusCode': 401,
        'body': 'Login failed'
    }
