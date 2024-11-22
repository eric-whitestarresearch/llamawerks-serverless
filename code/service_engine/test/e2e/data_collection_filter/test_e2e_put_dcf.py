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

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_data_collection_filter(data_collection_filter_single):
  BASE_URL = environ.get('API_BASE_URL')

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{data_collection_filter_single['pack_name']}/filter?filter_name={data_collection_filter_single['name']}")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200 #The fact that the dcf exists means the fixture was able to call the put. If we get something else it mean the fixiture was unable to create

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_data_collection_filter_bad_schema(data_collection_filter_single):
  BASE_URL = environ.get('API_BASE_URL')
  
  malformed_body = data_collection_filter_single['body']
  del malformed_body['name']
 
  data= bytes(dumps(malformed_body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{data_collection_filter_single['pack_name']}/filter", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  error_code = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
  
  #Should get a bad request with a malformed request
  assert error_code == 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_data_collection_filter_no_content_type():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  body = ""
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter", data=data, method='PUT')

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a media type not supported here
  assert error_code == 415

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_data_collection_filter_content_type_xml():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  body = ""
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter", data=data, method='PUT')
  req.add_header("Content-Type", "application/xml")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a media type not supported here
  assert error_code == 415

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_data_collection_filter_not_match(data_collection_filter_single):
  BASE_URL = environ.get('API_BASE_URL')
   
  data= dumps(data_collection_filter_single['body']).encode("utf-8")
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{data_collection_filter_single['pack_name']}qwe/filter", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a unprocessable entity when the pack_name in the URL and body don't match
  assert error_code == 422

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_data_collection_filter_dirty_input(data_collection_filter_single):
  BASE_URL = environ.get('API_BASE_URL')

  body = data_collection_filter_single['body']
  body['name'] = f"${body['name']}"
  
  data= dumps(body).encode("utf-8")
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{data_collection_filter_single['pack_name']}/filter", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a unprocessable entity when the definition includes a charcter that could indicate an injection attack
  assert error_code == 422