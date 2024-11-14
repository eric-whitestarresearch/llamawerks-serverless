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
  result = data_collection.create_data_collection(event, context)
  assert result['statusCode'] == 200 #The data collection already exists

  #Clean up after our selves
  event = {"pathParameters":{"pack_name": "blarf","data_collection_name":dc_name},"queryStringParameters":{}}
  result = data_collection.delete_data_collection(event,context)
  assert result['statusCode'] == 200