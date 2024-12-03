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
from json import dumps,loads
import random
import string

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_service_by_name(service_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  variables={'cat_name':'Boone','cat_info':{'name':"Boone","age":7}}
 
  data= bytes(dumps(variables).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{service_single['pack_name']}/service/{service_single['name']}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  try:
    assert response.getcode() == 201 #Successfully submitted
  finally:
    #Clean up the execution
    exeuction = loads(response.read().decode('utf-8'))
    req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{exeuction['id']}", data=data, method='DELETE')
    response = urllib.request.urlopen(req)

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_service_missing_vars(service_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  variables={'cat_name':'Boone'}
 
  data= bytes(dumps(variables).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{service_single['pack_name']}/service/{service_single['name']}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 

  assert error_code == 400 #Expected when variables are missing

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_service_by_name_not_exist():
  BASE_URL = environ.get('API_BASE_URL')
  service_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"

  variables={'cat_name':'Boone','cat_info':{'name':"Boone","age":7}}
 
  data= bytes(dumps(variables).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service/{service_name}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 

  assert error_code == 404 #Expect a not found because we never created it


@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_service__by_name_no_content_type():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  service_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = ""
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service/{service_name}", data=data, method='POST')

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 
    
  assert error_code == 415 #Expect a media type not supported

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_service_by_name_content_type_xml():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  service_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = ""
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service/{service_name}", data=data, method='POST')
  req.add_header("Content-Type", "application/xml")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 
    
  assert error_code == 415 #Expect a media type not supported

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_service_by_name_dirty_input():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  service_name = ''.join(random.choices(string.ascii_letters,k=10))
  
  body = {"$cat_name":"Axel"}
  
  data= dumps(body).encode("utf-8")
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service/{service_name}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a unprocessable entity when the definition includes a charcter that could indicate an injection attack
  assert error_code == 422

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_service_by_name_invalid_json():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  service_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = '{"a"}'
  
  data= body.encode("utf-8")
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service/{service_name}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get an error when the definition includes invalid json
  assert error_code == 400

