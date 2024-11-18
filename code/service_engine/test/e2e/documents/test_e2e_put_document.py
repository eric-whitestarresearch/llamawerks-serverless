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
def test_e2e_put_document(document_single):
  BASE_URL = environ.get('API_BASE_URL')

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200 #The fact that the document exists means the fixture was able to call the put. If we get something else it mean the fixiture was unable to create

#Skip this test for now, as schema check is not yet done on documents
# @pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
# def test_e2e_put_document_bad_schema(document_single):
#   BASE_URL = environ.get('API_BASE_URL')
  
#   malformed_body = document_single['body']
#   del malformed_body['name']
 
#   data= bytes(dumps(malformed_body).encode("utf-8"))
#   req = urllib.request.Request(f"{BASE_URL}/service_engine/{document_single['pack_name']}/data_collection/{document_single['data_collection_name']}", data=data, method='PUT')
#   req.add_header("Content-Type", "application/json")

#   error_code = None

#   try:
#     response = urllib.request.urlopen(req)
#   except urllib.error.HTTPError as e:
#     error_code = e.code 
  
#   #Should get a bad request with a malformed request
#   assert error_code == 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_document_data_collection_does_not_exist():
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = "blarf"
  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = ""

  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")
  
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 404 #Make sure we got a 404

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_document_no_content_type():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  data_collection_name = "asdf"
  body = ""
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}", data=data, method='PUT')

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a media type not supported here
  assert error_code == 415

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_document_content_type_xml():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  data_collection_name = "asdf"
  body = ""
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}", data=data, method='PUT')
  req.add_header("Content-Type", "application/xml")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a media type not supported here
  assert error_code == 415
