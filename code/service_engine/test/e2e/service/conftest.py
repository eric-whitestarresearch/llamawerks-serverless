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
def service_single():
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

  yield {"name": service_name, "pack_name": pack_name, "body": body}

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service?service_name={service_name}", method='DELETE')
  response = urllib.request.urlopen(req)

@pytest.fixture
def service_multi():
  BASE_URL = environ.get('API_BASE_URL')
  service_names = [''.join(random.choices(string.ascii_letters,k=10)),''.join(random.choices(string.ascii_letters,k=10)),''.join(random.choices(string.ascii_letters,k=10))]
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))

  services = []
  for service_name in service_names:
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

    response = urllib.request.urlopen(req) #Create

    services.append({"name": service_name, "pack_name": pack_name, "body": body})
    
  yield services

  for service_name in service_names:
    req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service?service_name={service_name}", method='DELETE')
    response = urllib.request.urlopen(req) #Delete 

@pytest.fixture
def service_renderable():
  BASE_URL = environ.get('API_BASE_URL')
  
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))

  #Create the data collection
  dc_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = {
    "name": dc_name,
    "pack": pack_name,
    "fields": [
      {
        "name": "name",
        "type": "string",
        "required": True,
        "index": True,
        "unique": True
      },{
        "name": "color",
        "type": "string",
        "required": True,
        "index": False,
        "unique": False
      },{
        "name": "age",
        "type": "integer",
        "required": True,
        "index": False,
        "unique": False
      }
    ]
  }
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)
  
  #Create some documents
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

  documents = []
  for doc_body in doc_bodies:
      
    doc_data = bytes(dumps(doc_body).encode("utf-8"))
    req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{dc_name}/document", data=doc_data, method='PUT')
    req.add_header("Content-Type", "application/json")

    response = urllib.request.urlopen(req)
    doc_id = loads(response.read().decode('utf-8'))

    documents.append({"data_collection_name": dc_name, "pack_name": pack_name, "doc_id": doc_id['id'], 'body': doc_body })

  #Create a filter
  filter_name_info = ''.join(random.choices(string.ascii_letters,k=10))
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
    "name": filter_name_info,
    "data_collection": dc_name,
    "project": [
      "name",
      "age"
    ]
  }
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  #Create a filter
  filter_name_age = ''.join(random.choices(string.ascii_letters,k=10))
  body = {
    "pack": pack_name,
    "filter": {
      "age": 7
    },
    "variables": [],
    "name": filter_name_age,
    "data_collection": dc_name,
    "project": ["name"]
  }
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)


  #Create the service
  service_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = {
    "name": service_name,
    "pack": pack_name,
    "fields": [{
        "index": 0,
        "name": "cat_name",
        "display_name": "Cat Name",
        "wait_to_render": False,
        "filter": filter_name_age,
        "data_collection": dc_name,
        "display_type": "drop_down",
        "selection_key": "name"
    },{
      "index": 1,
      "name": "cat_info",
      "display_name": "Cat Information",
      "wait_to_render": True,
      "filter": filter_name_info,
      "data_collection": dc_name,
      "display_type": "grid",
      "selection_key": "name"
  }]}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  yield {"name": service_name, "pack_name": pack_name, "body": body, 'dc_name': dc_name, 'documents': documents}

  #Clean up the documents
  for document in documents:
    req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{dc_name}/document/id/{document['doc_id']}", method='DELETE')
    response = urllib.request.urlopen(req) #Delete the document

  #Clean up the data collection
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection?data_collection_name={dc_name}", method='DELETE')
  response = urllib.request.urlopen(req)

  #Clean up the filters
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name_info}", method='DELETE')
  response = urllib.request.urlopen(req)
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name_age}", method='DELETE')
  response = urllib.request.urlopen(req)
  
  #Clean up the service
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service?service_name={service_name}", method='DELETE')
  response = urllib.request.urlopen(req)