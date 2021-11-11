import pandas as pd
import json

def lambda_handler(event, context):
    print('Hello from Lambda 2')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda5!')
    } 


