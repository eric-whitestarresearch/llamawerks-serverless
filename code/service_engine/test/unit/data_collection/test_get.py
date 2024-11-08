import data_collection
from os import environ
import pytest

@pytest.mark.skipif(environ.get('SKIP_LOCAL') != None, reason="local not enabled")
def test_get_data_collection():
  event = {"pathParameters":{"pack_name": "blarf"},"queryStringParameters":{ "data_collection_name": "blarf"}}
  context = None

  result = data_collection.get_data_collections(event, context)

  assert result['statusCode'] == 200

@pytest.mark.skipif(environ.get('SKIP_LOCAL') != None, reason="local not enabled")
def test_get_all_data_collection():
  event = {"pathParameters":{"pack_name": "blarf"},"queryStringParameters":{}}
  context = None

  result = data_collection.get_data_collections(event, context)

  assert result['statusCode'] == 200

@pytest.mark.skipif(environ.get('SKIP_LOCAL') != None, reason="local not enabled")
def test_get_data_collection_does_not_exist():
  event = {"pathParameters":{"pack_name": "blarf"},"queryStringParameters":{"data_collection_name": "asdfqwer"}}
  context = None

  result = data_collection.get_data_collections(event, context)

  assert result['statusCode'] == 404

@pytest.mark.skipif(environ.get('SKIP_LOCAL') != None, reason="local not enabled")
def test_get_data_collection_none_in_pack():
  event = {"pathParameters":{"pack_name": "lkjhoiu"},"queryStringParameters":{}}
  context = None

  result = data_collection.get_data_collections(event, context)

  assert result['statusCode'] == 204