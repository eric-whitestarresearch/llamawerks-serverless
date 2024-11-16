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
def document_single():
  BASE_URL = environ.get('API_BASE_URL')
  dc_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  dc_body = {
    "name": dc_name,
    "pack": pack_name,
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
      },
      {
        "name": "age",
        "type": "integer",
        "required": True,
        "index": False,
        "unique": False
      }
    ]
  }
 
  data= bytes(dumps(dc_body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  doc_body = {
    "name": "Boone",
    "color": "brown tabby",
    "age": 7
  }

  doc_data = bytes(dumps(doc_body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{dc_name}", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  doc_id = loads(response.read().decode('utf-8'))

  yield {"document_collection_name": dc_name, "pack_name": pack_name, "doc_id": doc_id['id']}

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{dc_name}/id/{doc_id['id']}", method='DELETE')
  response = urllib.request.urlopen(req) #Delete the document

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection?data_collection_name={dc_name}", method='DELETE')
  response = urllib.request.urlopen(req) #Delete the data collection

@pytest.fixture
def document_multi():
  BASE_URL = environ.get('API_BASE_URL')
  dc_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))

  doc_bodies = [
    {
      "name": "Boone",
      "color": "brown tabby",
      "age": 7
    },
    {
      "name": "Kaley",
      "color": "tortie",
      "age": 1
    }
  ]

  dc_body = {
    "name": dc_name,
    "pack": pack_name,
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
      },
      {
        "name": "age",
        "type": "integer",
        "required": True,
        "index": False,
        "unique": False
      }
    ]
  }
 
  data= bytes(dumps(dc_body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  documents = []
  for doc_body in doc_bodies:
      
    doc_data = bytes(dumps(doc_body).encode("utf-8"))
    req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{dc_name}", data=doc_data, method='PUT')
    req.add_header("Content-Type", "application/json")

    response = urllib.request.urlopen(req)
    doc_id = loads(response.read().decode('utf-8'))

    documents.append({"document_collection_name": dc_name, "pack_name": pack_name, "doc_id": doc_id['id'] })
    
  yield documents

  for document in documents:
    req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{dc_name}/id/{document['doc_id']}", method='DELETE')
    response = urllib.request.urlopen(req) #Delete the document

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection?data_collection_name={dc_name}", method='DELETE')
  response = urllib.request.urlopen(req) #Delete the data collection


@pytest.fixture
def empty_data_collection():
  BASE_URL = environ.get('API_BASE_URL')
  dc_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  dc_body = {
    "name": dc_name,
    "pack": pack_name,
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
      },
      {
        "name": "age",
        "type": "integer",
        "required": True,
        "index": False,
        "unique": False
      }
    ]
  }
 
  data= bytes(dumps(dc_body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  yield {"name": dc_name, "pack_name": pack_name, "data_collection_name": dc_name }

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection?data_collection_name={dc_name}", method='DELETE')
  response = urllib.request.urlopen(req) #Delete the data collection