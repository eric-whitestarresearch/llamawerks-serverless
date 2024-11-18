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

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_document(document_single):
  BASE_URL = environ.get('API_BASE_URL')

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}")
  response = urllib.request.urlopen(req)

  document_count = len(loads(response.read().decode('utf-8')))

  assert response.getcode() == 200 and document_count == 1 #We should only get one document here

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_all_documents(document_multi):
  BASE_URL = environ.get('API_BASE_URL')
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_multi[0]['pack_name']}/data_collection/{document_multi[0]['data_collection_name']}")
  response = urllib.request.urlopen(req)

  document_count = len(loads(response.read().decode('utf-8')))

  assert response.getcode() == 200 and document_count == len(document_multi)

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_document_data_collection_does_not_exist():
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = "blarf"
  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}")
  
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 404 #Make sure we got a 404

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_get_data_collection_none_in_pack(empty_data_collection):
  BASE_URL = environ.get('API_BASE_URL')
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{empty_data_collection['pack_name']}/data_collection/{empty_data_collection['data_collection_name']}")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 204