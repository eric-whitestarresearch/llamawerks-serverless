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
def test_e2e_patch_service(service_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  updated_body = service_single['body']
  updated_body['fields'].append({
      "name": "string",
      "display_name": "string",
      "wait_to_render": False,
      "filter": "string",
      "data_collection": "string",
      "display_type": "drop_down",
      "selection_key": "string"
  })
 
  data= bytes(dumps(updated_body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{service_single['pack_name']}/service", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  assert response.getcode() == 202 #Successfully updated

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_service_no_change(service_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  data= bytes(dumps(service_single['body']).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{service_single['pack_name']}/service", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  assert response.getcode() == 208 #No change

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_service_bad_schema(service_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  malformed_body = service_single['body']
  del malformed_body['name']
  response = None
  data= bytes(dumps(malformed_body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{service_single['pack_name']}/service", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 

  assert error_code == 400 #Expected when the schema conditions are not met

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_service_not_exist():
  BASE_URL = environ.get('API_BASE_URL')
  service_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"
  body =  {
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
    }]}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 

  assert error_code == 404 #Expect a not found because we never created it


@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_service_no_content_type():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  body = ""
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service", data=data, method='PATCH')

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 
    
  assert error_code == 415 #Expect a media type not supported

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_service_content_type_xml():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  body = ""
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service", data=data, method='PATCH')
  req.add_header("Content-Type", "application/xml")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 
    
  assert error_code == 415 #Expect a media type not supported

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_service_not_match(service_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  data= bytes(dumps(service_single['body']).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{service_single['pack_name']}asdf/service", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 

  assert error_code == 422 #Expect an unprocessable entity since the pack name in the URL and body don't match

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_service_dirty_input(service_single):
  BASE_URL = environ.get('API_BASE_URL')

  body = service_single['body']
  body['name'] = f"${body['name']}"
  
  data= dumps(body).encode("utf-8")
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{service_single['pack_name']}/service", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a unprocessable entity when the definition includes a charcter that could indicate an injection attack
  assert error_code == 422

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_service_invalid_json():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = '{"a"}'
  
  data= body.encode("utf-8")
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get an error when the definition includes invalid json
  assert error_code == 400

