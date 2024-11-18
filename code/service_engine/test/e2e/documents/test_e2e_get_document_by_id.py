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
from json import loads
from secrets import token_hex

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_document_by_id(document_multi):
  BASE_URL = environ.get('API_BASE_URL')

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_multi[0]['pack_name']}/data_collection/{document_multi[0]['data_collection_name']}/id/{document_multi[0]['doc_id']}")
  response = urllib.request.urlopen(req)

  retrieved_doc_id = loads(response.read().decode('utf-8'))['_id']['$oid']

  assert response.getcode() == 200 and retrieved_doc_id == document_multi[0]['doc_id'] #We should get back the document that was created

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_document_by_id_not_exist(document_single):
  BASE_URL = environ.get('API_BASE_URL')

  doc_id = token_hex(12) #12 Bytes gets us 24 hex characters
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}/id/{doc_id}")
  
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 404 #Make sure we got a 404

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_document_invalid_id(document_single):
  BASE_URL = environ.get('API_BASE_URL')

  doc_id = 'ww' + token_hex(11)
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}/id/{doc_id}")
  
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_document_invalid_id_too_long(document_single):
  BASE_URL = environ.get('API_BASE_URL')

  doc_id = token_hex(25)
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}/id/{doc_id}")
  
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_document_invalid_id_too_short(document_single):
  BASE_URL = environ.get('API_BASE_URL')

  doc_id = token_hex(3)
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}/id/{doc_id}")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400