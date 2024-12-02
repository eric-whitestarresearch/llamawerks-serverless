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
def test_e2e_patch_document_by_id(document_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  updated_body = {"document": document_single['body']}
  updated_body['document']['hair_length'] = 'short'
 
  data= bytes(dumps(updated_body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}/document/id/{document_single['doc_id']}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)
  
  update_count = loads(response.read().decode('utf-8'))

  assert response.getcode() == 200 and update_count['updated'] == 1 #Successfully updated

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document_by_id_no_change(document_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  updated_body = {"document": document_single['body']}
 
  data= bytes(dumps(updated_body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}/document/id/{document_single['doc_id']}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)
  
  update_count = loads(response.read().decode('utf-8'))

  assert response.getcode() == 200 and update_count['updated'] == 0 #No update because it was the same

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document_by_id_doc_not_exist(document_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  updated_body = {"document": document_single['body']}
  updated_body['document']['hair_length'] = 'short'
  doc_id = token_hex(12)
 
  data= bytes(dumps(updated_body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}/document/id/{doc_id}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)
  
  update_count = loads(response.read().decode('utf-8'))

  assert response.getcode() == 200 and update_count['updated'] == 0 #No document matched

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document_by_id_bad_schema(document_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  malformed_body = {"document2": document_single['body']}
 
  data= bytes(dumps(malformed_body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}/document/id/{document_single['doc_id']}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 

  assert error_code == 400 #Expected when the schema conditions are not met

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document_by_id_data_collection_not_exist():
  BASE_URL = environ.get('API_BASE_URL')
  doc_id = token_hex(12)
  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"
  body =  {"document": {}}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}/document/id/{doc_id}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 

  assert error_code == 404 #Expect a not found because we never created the data collection


@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document_by_id_no_content_type():
  BASE_URL = environ.get('API_BASE_URL')

  doc_id = token_hex(12)
  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"
  body =  {"document": {}}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}/document/id/{doc_id}", data=data, method='PATCH')

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 
    
  assert error_code == 415 #Expect a media type not supported

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_document_by_id_content_type_xml():
  BASE_URL = environ.get('API_BASE_URL')
  
  doc_id = token_hex(12)
  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"
  body =  {"document": {}}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}/document/id/{doc_id}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/xml")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 
    
  assert error_code == 415 #Expect a media type not supported

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document_by_id_dirty_input():
  BASE_URL = environ.get('API_BASE_URL')

  doc_id = token_hex(12)
  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"
  body =  {"document": {"$.bad":"nicetry"}}
  
  data= dumps(body).encode("utf-8")
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}/document/id/{doc_id}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a unprocessable entity when the definition includes a charcter that could indicate an injection attack
  assert error_code == 422

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document_by_id_invalid_json():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))
  doc_id = token_hex(12)

  body = '{"a"}'
  
  data= body.encode("utf-8")
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}/document/id/{doc_id}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get an error when the definition includes invalid json
  assert error_code == 400


