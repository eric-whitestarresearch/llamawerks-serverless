#     Llamaflow - A self service portal with runbook automation
#     Copyright (C) 2024  Whitestar Research LLC
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#      Unless required by applicable law or agreed to in writing, software
#      distributed under the License is distributed on an "AS IS" BASIS,
#      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#      See the License for the specific language governing permissions and
#      limitations under the License.

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