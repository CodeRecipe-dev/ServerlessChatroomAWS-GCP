import json
import os
import boto3
import time
from datetime import date
from lib.db import ConnectionsStore
from lib.messages_db import MessagesStore
from html_sanitizer import Sanitizer

def handle(event, context):
  ddb = boto3.resource('dynamodb')
  messages_table = MessagesStore(ddb)

  if "getAllMessages" in json.loads(event["body"]):
    connections_url = "https://"+event["requestContext"]["domainName"]+"/"+os.environ["Stage"]
    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url = connections_url)
    apigateway_response = gatewayapi.post_to_connection(ConnectionId=event["requestContext"]["connectionId"], Data=json.dumps(messages_table.get_messages()).encode('utf-8'))
    return {"statusCode": 200}

  connections_table = ConnectionsStore(ddb)
  data = {
    "connectionId": event["requestContext"]["connectionId"]
  }
  connections_ids = connections_table.get_connections()
  sanitizer = Sanitizer()
  chat_message = sanitizer.sanitize(json.loads(event["body"])["data"])

  lambda_client = boto3.client('lambda')
  analysis_handler_function_name = "{}-{}".format(os.environ["Stage"], "AnalysisHandler")
  response = lambda_client.invoke(FunctionName=analysis_handler_function_name,
                       InvocationType='RequestResponse',
                       Payload=json.dumps({"message":chat_message}))
  sentiment_response = response['Payload'].read().decode("utf-8")

  messageToSend = {
    "action": "sendMessage",
    "data": {"message": chat_message, "sentiment": sentiment_response}
  }

  message_data_for_ddb = {
    "date": date.today().strftime("%d-%m-%Y"),
    "timestamp": int(round(time.time() * 1000)),
    "message": messageToSend["data"]
  }
  messages_table.add_new_message(**message_data_for_ddb)

  for connection_id in connections_ids:
    connections_url = "https://"+event["requestContext"]["domainName"]+"/"+os.environ["Stage"]
    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url = connections_url)    
    apigateway_response = gatewayapi.post_to_connection(ConnectionId=connection_id['connectionId'], Data=json.dumps(messageToSend).encode('utf-8'))

  return {"statusCode": 200}