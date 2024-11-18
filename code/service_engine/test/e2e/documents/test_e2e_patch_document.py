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

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document(docuement_multi_with_filter):
  BASE_URL = environ.get('API_BASE_URL')

  body = {"variables": {"cat_name":"Boone"},
          "document":{"hair_length": "short"}
          }
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{docuement_multi_with_filter['pack_name']}/data_collection/{docuement_multi_with_filter['data_collection_name']}?filter_name={docuement_multi_with_filter['filter_name']}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)

  doc_updated = loads(response.read().decode('utf-8'))
 
  assert response.getcode() == 200 and doc_updated['updated'] == 1 #We updated 1 document




@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document_multiple(docuement_multi_with_filter_multi_match):
  BASE_URL = environ.get('API_BASE_URL')

  body = {"variables": {"age":7},
          "document":{"siblings": True}
          }
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{docuement_multi_with_filter_multi_match['pack_name']}/data_collection/{docuement_multi_with_filter_multi_match['data_collection_name']}?filter_name={docuement_multi_with_filter_multi_match['filter_name']}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)

  doc_updated = loads(response.read().decode('utf-8'))
 
  assert response.getcode() == 200 and doc_updated['updated'] == 2 #We updated 1 document

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document__no_match(docuement_multi_with_filter):
  BASE_URL = environ.get('API_BASE_URL')

  body = {"variables": {"cat_name":"Axel"},
          "document":{"hair_length": "short"}
          }
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{docuement_multi_with_filter['pack_name']}/data_collection/{docuement_multi_with_filter['data_collection_name']}?filter_name={docuement_multi_with_filter['filter_name']}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)

  doc_updated = loads(response.read().decode('utf-8'))
 
  assert response.getcode() == 200 and doc_updated['updated'] == 0 #We updated no document

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document_var_dont_match(docuement_multi_with_filter):
  BASE_URL = environ.get('API_BASE_URL')

  body = {"variables": {"age":4},
          "document":{"hair_length": "short"}
          }
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{docuement_multi_with_filter['pack_name']}/data_collection/{docuement_multi_with_filter['data_collection_name']}?filter_name={docuement_multi_with_filter['filter_name']}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400
@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document_filter_not_exist(docuement_multi_with_filter):
  BASE_URL = environ.get('API_BASE_URL')

  body = {"variables": {"cat_name":"Boone"},
          "document":{"hair_length": "short"}
          }
  filter_name = ''.join(random.choices(string.ascii_letters,k=10))

  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{docuement_multi_with_filter['pack_name']}/data_collection/{docuement_multi_with_filter['data_collection_name']}?filter_name={filter_name}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")
  
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 404 #Make sure we got a 404


@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document_data_collection_does_not_exist():
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = "blarf"
  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))
  filter_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = {"variables": {"cat_name":"Boone"},
          "document":{"hair_length": "short"}
          }

  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}?filter_name={filter_name}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/json")
  
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 404 #Make sure we got a 404

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document_no_content_type():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  data_collection_name = "asdf"
  filter_name = "asdf"
  body = {}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}?filter_name={filter_name}", data=data, method='PATCH')

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a media type not supported here
  assert error_code == 415

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_patch_document_content_type_xml():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  data_collection_name = "asdf"
  filter_name = "asdf"
  body = {}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}?filter_name={filter_name}", data=data, method='PATCH')
  req.add_header("Content-Type", "application/xml")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a media type not supported here
  assert error_code == 415
