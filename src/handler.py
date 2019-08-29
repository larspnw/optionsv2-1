import boto3
import json
from boto3.dynamodb.conditions import Attr

print('Loading function')
dynamo = boto3.client('dynamodb')
table_name = "Options"
#table_name = os.environ['TABLE_NAME']

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def expiredOptions_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    operation = event['httpMethod']
    #resourcePath = event['requestContext']['resourcePath']
    if operation == 'GET':
        payload = event['queryStringParameters']
        return doExpired(payload)
    else:
        return respond(None, "{'message:', 'Not supported ' }")

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(TableName=table_name, **x),
        'GET': lambda dynamo, x: dynamo.scan(TableName=table_name, **x) if x else dynamo.scan(TableName=table_name),
        'POST': lambda dynamo, x: dynamo.put_item(TableName=table_name, **x),
        'PUT': lambda dynamo, x: dynamo.update_item(TableName=table_name, **x),
    }

    operation = event['httpMethod']
    #resourcePath = event['requestContext']['resourcePath']
    #print("resourcePath: " + resourcePath)

    if operation == 'GET':
        payload = event['queryStringParameters']
        return doGet(payload)
    else:
        return respond(None, "{'message:', 'Not supported '}")

def doGet(payload):
    print("doGet enter ", payload)
    #r = dynamo.scan(TableName=table_name)
    if payload == None:
        r = dynamo.scan(TableName=table_name)
    #else:
        #r = dynamo.scan(TableName=table_name, payload)

    return respond(None, r)

def doExpired(payload):
    print("doExpired enter ", payload)
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('Options')
    #TODO fix date
    now = "2019/08/28"
    r = table.scan(TableName=table_name,
                    FilterExpression=Attr('expirationDate').lt(now))
    #return respond(None, "{'message:', 'get expired'}")
    return respond(None, r)
    #TODO error handling
