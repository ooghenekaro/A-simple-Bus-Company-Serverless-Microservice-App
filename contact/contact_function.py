def lambda_handler(event, context):
    # Normally, process contact request
    headers = {
        "Access-Control-Allow-Origin": "*",  # Allows all origins
        "Access-Control-Allow-Credentials": "true",  # Allows credentials (cookies, headers, etc.)
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",  # Allows these headers
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"  # Allows these HTTP methods
    }
    return {
        'statusCode': 200,
        'body': 'Thank you for contacting us! We will get back to you soon.'
    }
