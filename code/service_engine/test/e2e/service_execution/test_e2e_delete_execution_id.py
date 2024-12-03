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
from json import loads
import string
from secrets import token_hex

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_delete_execution(service_execution_single):
  BASE_URL = environ.get('API_BASE_URL')

  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{service_execution_single['execution_id']}", method='DELETE')
  response = urllib.request.urlopen(req)

  del_count = loads(response.read().decode('utf-8'))

  assert response.getcode() == 200 and del_count['deleted'] == 1

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_delete_execution_resubmit(service_execution_single):
  BASE_URL = environ.get('API_BASE_URL')

  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{service_execution_single['execution_id']}", method='DELETE')
  response = urllib.request.urlopen(req)

  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{service_execution_single['execution_id']}", method='DELETE')
  response = urllib.request.urlopen(req)

  del_count = loads(response.read().decode('utf-8'))

  assert response.getcode() == 200 and del_count['deleted'] == 0 #Should not have deleted anything the second time

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_delete_execution_does_not_exist():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(12)
  pack_name = "blarf"
  service_name = ''.join(random.choices(string.ascii_letters,k=10))
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", method='DELETE')
  response = urllib.request.urlopen(req)

  del_count = loads(response.read().decode('utf-8'))

  assert response.getcode() == 200 and del_count['deleted'] == 0 #Nothing to delete

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_delete_execution_invalid_id():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = 'ww' + token_hex(11)
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", method='DELETE')
  
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_execution_invalid_id_too_long():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(25)
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", method='DELETE')
  
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_execution_invalid_id_too_short():
  BASE_URL = environ.get('API_BASE_URL')

  execution_id = token_hex(3)
  req = urllib.request.Request(f"{BASE_URL}/service_engine/execution/id/{execution_id}", method='DELETE')

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400