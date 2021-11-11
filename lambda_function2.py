import json
import boto3
from base64 import b64encode
import urllib3


def lambda_handler(event, context):
    
    print('Event')
    print(event)
   
    
    #get query
    q = event['queryStringParameters']['q']
    print('query:')
    print(q)
    
    client = boto3.client('lexv2-runtime', region_name='us-east-1')
    
     #parse it with lex

    '''

    response = client.recognize_text(
        botId='Y5RTYYRDLS',
        botAliasId='TSTALIASID',
        localeId='en_US',
        sessionId="user_session",
        text=str(q))  
    
    print('response of lexbot:')    
    print(response)
    
    if response['interpretations'][0]['intent']['name'] == "SearchIntent":
        slots = response['interpretations'][0]['intent']['slots']
    else:
        slots = response['interpretations'][1]['intent']['slots']
    
    print('print slots:')
    print(slots)
    
    res = []
    if slots['photo_tag']:
        res.append(slots['photo_tag']['value']['interpretedValue'])
    if slots['photo_tag2']:
        res.append(slots['photo_tag2']['value']['interpretedValue'])
    if slots['photo_tag3']:
        res.append(slots['photo_tag3']['value']['interpretedValue'])
        
    labels = list(set(res))
    print('extracted labels:')
    print(labels)

    '''
    
    http = urllib3.PoolManager()    
    userAndPass = b64encode(b"admin:Vamosroberto100%").decode("ascii")
    headers = { 'Authorization' : 'Basic %s' %  userAndPass }
    
    #retrieve names with elasticSearch
    
    '''
    url = 'https://search-photos-m462xed766ciaehgsrrwsywkjq.us-east-2.es.amazonaws.com/photos/_search?q='
    resp = []
    if labels:
        for label in labels:
            if (label is not None) and label != '':
                url2 = url+label
                r = http.request('GET',url2, headers=headers)
                if r:
                    resp.append(json.loads(r.data))
    print('response of opensearch:')
    print(resp)
    
    output = []
    for r in resp:
        if 'hits' in r:
             for val in r['hits']['hits']:
                key = val['_source']['objectKey']
                if key not in output:
                    output.append(key)
                    
    print('extracted keys:')
    print(output)

    '''
    ret_body = {}

    '''
    for i,e in enumerate(output):
        ret_body['k'+str(i)] = e
    
    
    #send them back as body
    
    
    '''
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'http://hw2b101.s3-website.us-east-2.amazonaws.com',
            'Access-Control-Allow-Methods': 'OPTIONS, GET'
        },
        'body': json.dumps(ret_body)
    }


