import data_collection
from json import dumps
import random
import string
from os import environ
import pytest

@pytest.mark.skipif(environ.get('SKIP_LOCAL') != None, reason="local not enabled")
def test_put_delete_data_collection():
  event = {"pathParameters":{"pack_name": "blarf"},"queryStringParameters":{}}
  dc_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = {
  "name": dc_name,
  "pack": "blarf",
  "fields": [
    {
      "name": "name",
      "type": "string",
      "required": True,
      "index": True,
      "unique": True
    }
  ]}
  event['body'] = dumps(body)
  context = None

  result = data_collection.create_data_collection(event, context)
  assert result['statusCode'] == 201

  body = {
  "name": dc_name,
  "pack": "blarf",
  "fields": [
    {
      "name": "name",
      "type": "string",
      "required": True,
      "index": True,
      "unique": True
    },
    {
      "name": "color",
      "type": "string",
      "required": True,
      "index": False,
      "unique": False
    }
  ]}
  event['body'] = dumps(body)
  result = data_collection.update_data_collection(event, context)
  assert result['statusCode'] == 202 

  result = data_collection.update_data_collection(event, context)
  assert result['statusCode'] == 208 #There is no change
  
  #Clean up after our selves
  event = {"pathParameters":{"pack_name": "blarf","data_collection_name":dc_name},"queryStringParameters":{}}
  result = data_collection.delete_data_collection(event,context)
  assert result['statusCode'] == 200