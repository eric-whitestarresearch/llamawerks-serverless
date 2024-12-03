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
from time import time

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_exeuction(service_execution_multi):
  BASE_URL = environ.get('API_BASE_URL')

  body =  {"pack":service_execution_multi['pack_name']}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)
 
  execution_count = len(loads(response.read().decode('utf-8')))

  assert response.getcode() == 200 and execution_count == len(service_execution_multi['execution_ids'])

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_exeuction_all_parameters(service_execution_multi):
  BASE_URL = environ.get('API_BASE_URL')

  body =  {"status":['submitted', 'in progress'],
          "document_id": service_execution_multi['execution_ids'][0],
          "pack":service_execution_multi['pack_name'],
          "service_name": service_execution_multi['name'],
          "before": (int(time())),
          "after": (int(time())-(10*60)),
          "fields":['status', 'document_id','service_name']}
  
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)
 
  execution_count = len(loads(response.read().decode('utf-8')))

  assert response.getcode() == 200 and execution_count == 1

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_exeuction_before(service_execution_multi):
  BASE_URL = environ.get('API_BASE_URL')

  body =  {"status":['submitted', 'in progress'],
          "pack":service_execution_multi['pack_name'],
          "service_name": service_execution_multi['name'],
          "before": (int(time()))}
  
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)
 
  execution_count = len(loads(response.read().decode('utf-8')))

  assert response.getcode() == 200 and execution_count == len(service_execution_multi['execution_ids'])

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_exeuction_after(service_execution_multi):
  BASE_URL = environ.get('API_BASE_URL')

  body =  {"status":['submitted', 'in progress'],
          "pack":service_execution_multi['pack_name'],
          "service_name": service_execution_multi['name'],
          "after": (int(time())-(10*60))}
  
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)
 
  execution_count = len(loads(response.read().decode('utf-8')))

  assert response.getcode() == 200 and execution_count == len(service_execution_multi['execution_ids']) 
@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_exeuction_none_match(service_execution_multi):
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  body =  {"pack":pack_name}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
 
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 404

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_exeuction_invalid_schema(service_execution_multi):
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  body =  {"status":["asdf"]}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
 
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_exeuction_invalid_before_time(service_execution_multi):
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  body =  {"before":100.7}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
 
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_exeuction_invalid_after_time(service_execution_multi):
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  body =  {"after":"asdf"}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
 
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400


@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_id_invalid_id():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = 'ww' + token_hex(11)
  body =   {"document_id":execution_id}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_too_long():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(16)
  body =   {"document_id":execution_id}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_execution_too_short():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(3)
  body =   {"document_id":execution_id}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
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
  body =   {"document_id":execution_id}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')

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
  body =   {"document_id":execution_id}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
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

  body =   {"pack":"$badstuff"}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
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
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get an error when the definition includes invalid json
  assert error_code == 400