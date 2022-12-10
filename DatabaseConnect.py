import boto3
import json

def GetData(client_id):
    client = boto3.resource("dynamodb")
    table = client.Table("YouTuebApi")

    resp = table.get_item(
        Key={
            'client_id' : client_id
            }
        )
    return resp

def PutData(creds):
    credsJson = creds.to_json()
    credsDict   = json.loads(credsJson) 
    client = boto3.resource("dynamodb")
    table = client.Table("YouTuebApi")
    resp = table.put_item( Item= credsDict )
    return resp
