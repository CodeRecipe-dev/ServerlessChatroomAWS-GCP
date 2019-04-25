import boto3
from lib.db import ConnectionsStore

def handle(event, context):
  ddb = boto3.resource('dynamodb')
  connections_table = ConnectionsStore(ddb)
  data = {
    "connectionId": event["requestContext"]["connectionId"]
  }
  connections_table.add_new_connection(**data)
  return {"statusCode": 200}