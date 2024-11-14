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
import string
from json import dumps, loads

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_data_collection_filter():
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
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name}")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200 #It exists

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name}", method='DELETE')
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200 #Deleted

  del_count = loads(response.read().decode('utf-8'))

  assert del_count['deleted'] == 1 #data collection dilter was deleted

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_all_data_collection_filters():
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

  body['name'] = f"{filter_name}2"

  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  assert response.getcode() == 201 #Successfully created
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200

  filer_count = len(loads(response.read().decode('utf-8')))

  assert filer_count >= 2 #We should have atleast the two filters we created

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name}", method='DELETE')
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200 #Deleted filter 1

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name}2", method='DELETE')
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200 #Deleted filter 2

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_data_collection_dilter_does_not_exist():
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = "blarf"
  data_collection_name = "poiuasdf123"
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection?data_collection_name={data_collection_name}")
  response = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    if e.code == 404:
      assert True
    else:
      #We got an error, but it is not a 404 as expected
      assert False
  
  #If we have a response that means we got data back, which is not expected here
  if response != None:
    assert False
@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_get_data_collection_filter_not_exist():
  BASE_URL = environ.get('API_BASE_URL')
  
  pack_name = "blarf"
  filter_name = ''.join(random.choices(string.ascii_letters,k=10))
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name}")
  response = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    if e.code == 404:
      assert True #We expect this when the filter does not exist
    else:
      #We got an error, but it is not a 404 as expected
      assert False
    
  #If we have a response that means we got data back, which is not expected here
  if response != None:
    assert False

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_get_data_collection_filter_none_in_pack():
  BASE_URL = environ.get('API_BASE_URL')
  
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 204 #With a random pack there should be no filters


