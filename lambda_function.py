import json
import urllib3
from base64 import b64encode
import boto3
import datetime


def lambda_handler(event, context):
    # TODO implement
    #test for pipeline
    
    print('event')
    print(event)
    
    http = urllib3.PoolManager()
    userAndPass = b64encode(b"admin:Vamosroberto100%").decode("ascii")
    headers = { 'Authorization' : 'Basic %s' %  userAndPass, 'Content-Type': 'application/json'}
    
    #Extract image name
    name = event['Records'][0]['s3']['object']['key']
    #name = 'sad_dog.png'
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(u'hw2b2cf') 
    obj = bucket.Object(key=name)
    print('object')
    print(obj)
    response = obj.get()     #get Response
    print('response')
    print(response)
    
    mlist = json.loads(response['Metadata']['customlabels'])
    mlist = [e.upper() for e in mlist]
    
    
    client=boto3.client('rekognition')
    
    new_response = client.detect_labels(Image={'S3Object': {'Bucket': 'hw2b2cf', 'Name': name}}, MinConfidence=98)
    
   
    
    #parse labels
    print('new response')
    print(new_response)
    
    mlist2 = [e['Name'].upper() for e in new_response['Labels']]
    print(mlist2)
    
    tlist = list(set(mlist+mlist2))
    print(tlist)
    
    encoded_body = json.dumps({
        "objectKey": name,
        "bucket": "hw2b2cf",
        "createdTimestamp": str(datetime.datetime.now()),
        "labels": tlist,
    })
    
    
    r = http.request('POST', 
    'https://search-photos-m462xed766ciaehgsrrwsywkjq.us-east-2.es.amazonaws.com/photos/_doc', 
    headers=headers,
    body=encoded_body)
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Finished!')
    }
