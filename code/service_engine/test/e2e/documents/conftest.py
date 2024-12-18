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
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{dc_name}/document", data=doc_data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  doc_id = loads(response.read().decode('utf-8'))

  yield {"data_collection_name": dc_name, "pack_name": pack_name, "doc_id": doc_id['id'], 'body': doc_body}

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{dc_name}/document/id/{doc_id['id']}", method='DELETE')
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
      "name": "Cheyenne",
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
    req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{dc_name}/document", data=doc_data, method='PUT')
    req.add_header("Content-Type", "application/json")

    response = urllib.request.urlopen(req)
    doc_id = loads(response.read().decode('utf-8'))

    documents.append({"data_collection_name": dc_name, "pack_name": pack_name, "doc_id": doc_id['id'], 'body': doc_body })
    
  yield documents

  for document in documents:
    req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{dc_name}/document/id/{document['doc_id']}", method='DELETE')
    response = urllib.request.urlopen(req) #Delete the document

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection?data_collection_name={dc_name}", method='DELETE')
  response = urllib.request.urlopen(req) #Delete the data collection

@pytest.fixture
def docuement_multi_with_filter(document_multi):
  BASE_URL = environ.get('API_BASE_URL')
  filter_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = document_multi[0]['pack_name']
  data_collection_name = document_multi[0]['data_collection_name']
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

  yield {"filter_name": filter_name, "pack_name": pack_name, "data_collection_name": data_collection_name}

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name}", method='DELETE')
  response = urllib.request.urlopen(req)

@pytest.fixture
def docuement_multi_with_filter_multi_match(document_multi):
  BASE_URL = environ.get('API_BASE_URL')
  filter_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = document_multi[0]['pack_name']
  data_collection_name = document_multi[0]['data_collection_name']
  body = {
    "pack": pack_name,
    "filter": {
      "age": "#age#"
    },
    "variables": [
      {
        "name": "age",
        "type": "integer"
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

  yield {"filter_name": filter_name, "pack_name": pack_name, "data_collection_name": data_collection_name}

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name}", method='DELETE')
  response = urllib.request.urlopen(req)

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