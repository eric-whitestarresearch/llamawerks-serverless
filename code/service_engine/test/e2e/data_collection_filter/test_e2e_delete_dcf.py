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


import urllib.parse
import urllib.request
from os import environ
import pytest
from json import dumps, loads
import random
import string

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_delete_data_collection_filter_resubmit():
  BASE_URL = environ.get('API_BASE_URL')
  
  pack_name = "blarf"
  filter_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = {
    "pack": "blarf",
    "filter": {
      "name": "#cat_name#"
    },
    "variables": [
      {
        "name": "cat_name",
        "type": "string"
      }
    ],
    "name": filter_name,
    "data_collection": "blarf",
    "project": [
      "name",
      "age"
    ]
  }

  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  assert response.getcode() == 201 #Successfully created

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name}", method='DELETE')
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200 #Deleted

  del_count = loads(response.read().decode('utf-8'))

  assert del_count['deleted'] == 1 #data collection filter was deleted

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name}", method='DELETE')
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200 #Delete ok

  del_count = loads(response.read().decode('utf-8'))

  assert del_count['deleted'] == 0 #data collection already deleted


@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_delete_data_collection_filter_not_exist():
  BASE_URL = environ.get('API_BASE_URL')
  filter_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name}", method='DELETE')
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200 #Delete ok

  del_count = loads(response.read().decode('utf-8'))

  assert del_count['deleted'] == 0 #The data collection did not exist

