import json
import os
import requests
import jwt
import time

def handle(event, context):
  chat_message = event["message"]
  signed_jwt = _get_signed_jwt()
  sentiment_response = _get_sentiment_response(chat_message, signed_jwt)
  return sentiment_response

def _get_signed_jwt():
  iat = time.time()
  exp = iat + 3600
  payload = {'iss': os.environ["GCP_CLIENT_EMAIL_FROM_JSON"],
           'sub': os.environ["GCP_CLIENT_EMAIL_FROM_JSON"],
           'aud': 'https://language.googleapis.com/google.cloud.language.v1.LanguageService',
           'iat': iat,
           'exp': exp}
  additional_headers = {'kid': os.environ["GCP_PRIVATE_KEY_ID_FROM_JSON"]}
  signed_jwt = jwt.encode(payload, os.environ["GCP_PRIVATE_KEY_FROM_JSON"], headers=additional_headers,
                       algorithm='RS256')
  return signed_jwt

def _get_sentiment_response(chat_message, signed_jwt):
  data = {'encodingType': 'UTF8','document': {'type': 'PLAIN_TEXT','content': chat_message}}
  headers = {'Authorization': 'Bearer '+signed_jwt, 'Content-Type':'application/json; charset=utf-8'}
  response = requests.post("https://language.googleapis.com/v1/documents:analyzeSentiment", data=json.dumps(data), headers=headers)
  return response.json()