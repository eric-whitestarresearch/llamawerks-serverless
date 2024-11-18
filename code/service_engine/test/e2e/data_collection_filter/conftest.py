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
def data_collection_filter_single():
  BASE_URL = environ.get('API_BASE_URL')
  filter_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = {
    "pack": pack_name,
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
    "data_collection": data_collection_name,
    "project": [
      "name",
      "age"
    ]
  }
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  yield {"name": filter_name, "pack_name": pack_name, "data_collection_name": data_collection_name, "body": body}

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name}", method='DELETE')
  response = urllib.request.urlopen(req)

@pytest.fixture
def data_collection_filter_multi():
  BASE_URL = environ.get('API_BASE_URL')
  filter_names = [''.join(random.choices(string.ascii_letters,k=10)),''.join(random.choices(string.ascii_letters,k=10)),''.join(random.choices(string.ascii_letters,k=10))]
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))

  data_collection_filters = []
  for filter_name in filter_names:
    body = {
      "pack": pack_name,
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
      "data_collection": data_collection_name,
      "project": [
        "name",
        "age"
      ]
    }
  
    data= bytes(dumps(body).encode("utf-8"))
    req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter", data=data, method='PUT')
    req.add_header("Content-Type", "application/json")

    response = urllib.request.urlopen(req) #Create

    data_collection_filters.append({"name": filter_name, "pack_name": pack_name, "data_collection_name": data_collection_name, "body": body})
    
  yield data_collection_filters

  for filter_name in filter_names:
    req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name}", method='DELETE')
    response = urllib.request.urlopen(req) #Delete 

