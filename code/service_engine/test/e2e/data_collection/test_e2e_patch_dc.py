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
from json import dumps
import random
import string

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_data_collection(data_collection_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  updated_body = data_collection_single['body']
  updated_body['fields'].append({
    "name": "color",
    "type": "string",
    "required": True,
    "index": False,
    "unique": False
  })
 
  data= bytes(dumps(updated_body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{data_collection_single['pack_name']}/data_collection", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  assert response.getcode() == 202 #Successfully updated

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_data_collection_no_change(data_collection_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  data= bytes(dumps(data_collection_single['body']).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{data_collection_single['pack_name']}/data_collection", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  assert response.getcode() == 208 #No change

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_data_collection_bad_schema(data_collection_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  malformed_body = data_collection_single['body']
  del malformed_body['name']
  response = None
  data= bytes(dumps(malformed_body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{data_collection_single['pack_name']}/data_collection", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 

  assert error_code == 400 #Expected when the schema conditions are not met

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_data_collection_not_exist():
  BASE_URL = environ.get('API_BASE_URL')
  dc_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"
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
    ]
  }
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 

  assert error_code == 404 #Expect a not found because we never created it


@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_data_collection_no_content_type():
  BASE_URL = environ.get('API_BASE_URL')
  dc_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"
  body = ""
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection", data=data, method='PATCH')

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 
    
  assert error_code == 415 #Expect a media type not supported

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_data_collection_content_type_xml():
  BASE_URL = environ.get('API_BASE_URL')
  dc_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"
  body = ""
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection", data=data, method='PATCH')
  req.add_header("Content-Type", "application/xml")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 
    
  assert error_code == 415 #Expect a media type not supported

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_data_collection_not_match(data_collection_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  data= bytes(dumps(data_collection_single['body']).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{data_collection_single['pack_name']}asdf/data_collection", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 

  assert error_code == 422 #Expect an unprocessable entity since the pack name in the URL and body don't match

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_data_collection_dirty_input(data_collection_single):
  BASE_URL = environ.get('API_BASE_URL')

  body = data_collection_single['body']
  body['name'] = f"${body['name']}"
  
  data= dumps(body).encode("utf-8")
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{data_collection_single['pack_name']}/data_collection", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a unprocessable entity when the definition includes a charcter that could indicate an injection attack
  assert error_code == 422

