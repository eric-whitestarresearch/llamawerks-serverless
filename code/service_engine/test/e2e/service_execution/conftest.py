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

import urllib.request
from os import environ
import pytest
import random
from json import dumps, loads
import string

@pytest.fixture
def service_execution_single():
  BASE_URL = environ.get('API_BASE_URL')
  service_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = {
    "name": service_name,
    "pack": pack_name,
    "fields": [{
        "index": 0,
        "name": "cat_name",
        "display_name": "Cat Name",
        "wait_to_render": False,
        "filter": "has_not_been_fed",
        "data_collection": "cats",
        "display_type": "drop_down",
        "selection_key": "name"
    },
    {
      "index": 1,
      "name": "cat_info",
      "display_name": "Cat Information",
      "wait_to_render": True,
      "filter": "cat_name",
      "data_collection": "cats",
      "display_type": "grid",
      "selection_key": "name"
  }]}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  variables={'cat_name':'Boone','cat_info':{'name':"Boone","age":7}}
 
  data= bytes(dumps(variables).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service/{service_name}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)
  exeuction = loads(response.read().decode('utf-8'))
    
  yield {"name": service_name, "pack_name": pack_name, "body": body, "execution_id": exeuction['id']}

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service?service_name={service_name}", method='DELETE')
  response = urllib.request.urlopen(req)

  #Clean up the execution  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{exeuction['id']}", method='DELETE')
  response = urllib.request.urlopen(req)


@pytest.fixture
def service_execution_multi():
  BASE_URL = environ.get('API_BASE_URL')
  service_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = {
    "name": service_name,
    "pack": pack_name,
    "fields": [{
        "index": 0,
        "name": "cat_name",
        "display_name": "Cat Name",
        "wait_to_render": False,
        "filter": "has_not_been_fed",
        "data_collection": "cats",
        "display_type": "drop_down",
        "selection_key": "name"
    },
    {
      "index": 1,
      "name": "cat_info",
      "display_name": "Cat Information",
      "wait_to_render": True,
      "filter": "cat_name",
      "data_collection": "cats",
      "display_type": "grid",
      "selection_key": "name"
  }]}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  variables={'cat_name':'Boone','cat_info':{'name':"Boone","age":7}}
 
  data= bytes(dumps(variables).encode("utf-8"))

  execution_ids =[]
  for i in range(0,3):
    req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service/{service_name}", data=data, method='POST')
    req.add_header("Content-Type", "application/json")

    response = urllib.request.urlopen(req)
    execution_ids.append(loads(response.read().decode('utf-8'))['id'])
    
  yield {"name": service_name, "pack_name": pack_name, "body": body, "execution_ids": execution_ids}

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service?service_name={service_name}", method='DELETE')
  response = urllib.request.urlopen(req)

  for i in execution_ids:
    #Clean up the execution  
    req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{i}", method='DELETE')
    response = urllib.request.urlopen(req)

