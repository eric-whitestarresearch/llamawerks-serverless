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
def test_e2e_delete_document_by_id(document_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}/id/{document_single['doc_id']}", method='DELETE')
  response = urllib.request.urlopen(req)

  del_count = loads(response.read().decode('utf-8'))

  assert response.getcode() == 200 and del_count['deleted'] == 1

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_delete_document_by_id_resubmit(document_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}/id/{document_single['doc_id']}", method='DELETE')
  response = urllib.request.urlopen(req)

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}/id/{document_single['doc_id']}", method='DELETE')
  response = urllib.request.urlopen(req)

  del_count = loads(response.read().decode('utf-8'))

  assert response.getcode() == 200 and del_count['deleted'] == 0 #data collection already deleted


@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_delete_docuemnt_not_exist(document_single):
  BASE_URL = environ.get('API_BASE_URL')
 
  doc_id = token_hex(12)

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}/id/{doc_id}", method='DELETE')
  response = urllib.request.urlopen(req)

  del_count = loads(response.read().decode('utf-8'))

  assert response.getcode() == 200  and del_count['deleted'] == 0 #The data collection did not exist

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_delete_document_by_id_data_collection_not_exist():
  BASE_URL = environ.get('API_BASE_URL')
  doc_id = token_hex(12)
  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"
  doc_id = token_hex(12)
 
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}/id/{doc_id}", method='DELETE')

  error_code = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 

  assert error_code == 404 #Expect a not found because we never created the data collection

