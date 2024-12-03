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
from secrets import token_hex

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_exeuction_id(service_execution_single):
  BASE_URL = environ.get('API_BASE_URL')

  body =  {"status":"in progress"}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{service_execution_single['execution_id']}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)
 
  assert response.getcode() == 202

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_exeuction_id_with_step(service_execution_single):
  BASE_URL = environ.get('API_BASE_URL')

  body =  {"status":"in progress",
           "result": {
             "step": "step1",
             "status": "complete",
             "output": "123",
             "error": ""
           }}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{service_execution_single['execution_id']}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)
 
  assert response.getcode() == 202


@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_id_invalid_status():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(12)
  body =  {"status":"jkhlkjh"}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400
@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_id_missing_status():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(12)
  body =  {"result": {
             "step": "step1",
             "status": "complete",
             "output": "123",
             "error": ""
           }}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_id_result_not_match_schema():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(12)
  body =  {"status": "in progess",
          "result": {
             "step": "step1",
             "status": "complete",
             "output": "123"
           }}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_id_result_invalid_status():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(12)
  body =  {"status": "in progess",
          "result": {
             "step": "step1",
             "status": "asdf",
             "output": "123"
           }}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400


@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_id_not_exist():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(12)
  body =   {"status":"in progress"}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 404 #Make sure we got a 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_id_invalid_id():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = 'ww' + token_hex(11)
  body =   {"status":"in progress"}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_id_too_long():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(16)
  body =   {"status":"in progress"}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_id_too_short():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(3)
  body =   {"status":"in progress"}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400


@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_id_no_content_type():
  BASE_URL = environ.get('API_BASE_URL')
  
  execution_id = token_hex(12)
  body =   {"status":"in progress"}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", data=data, method='POST')

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a media type not supported here
  assert error_code == 415

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_id_content_type_xml():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(12)
  body =   {"status":"in progress"}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", data=data, method='POST')
  req.add_header("Content-Type", "application/xml")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a media type not supported here
  assert error_code == 415

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_id_dirty_input():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(12)
  body =   {"status":"in progress",
            "result": {
              "step": "$$money",
              "status": "complete",
              "output" : "qewr",
              "error": ""
            }}
  
  data= dumps(body).encode("utf-8")
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a unprocessable entity when the definition includes a charcter that could indicate an injection attack
  assert error_code == 422

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_invalid_json():
  BASE_URL = environ.get('API_BASE_URL')
  
  execution_id = token_hex(12)
  body = '{"a"}'
  
  data= body.encode("utf-8")
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get an error when the definition includes invalid json
  assert error_code == 400