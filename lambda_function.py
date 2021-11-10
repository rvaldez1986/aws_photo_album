import pandas as pd
import json

def lambda_hadler(event, context):
    print('Hello from Lambda')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    } 
