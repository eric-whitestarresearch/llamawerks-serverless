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
def test_e2e_post_document_project_true(docuement_multi_with_filter):
  BASE_URL = environ.get('API_BASE_URL')

  body =  {"cat_name":"Boone"}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{docuement_multi_with_filter['pack_name']}/data_collection/{docuement_multi_with_filter['data_collection_name']}/document?filter_name={docuement_multi_with_filter['filter_name']}&project=true", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)

  doc_count = loads(response.read().decode('utf-8'))
 
  assert response.getcode() == 200 and len(doc_count) == 1 #We found 1 document

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_document_project_true_multi_result(docuement_multi_with_filter_multi_match):
  BASE_URL = environ.get('API_BASE_URL')

  body =  {"age":7}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{docuement_multi_with_filter_multi_match['pack_name']}/data_collection/{docuement_multi_with_filter_multi_match['data_collection_name']}/document?filter_name={docuement_multi_with_filter_multi_match['filter_name']}&project=true", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)

  doc_count = loads(response.read().decode('utf-8'))
 
  assert response.getcode() == 200 and len(doc_count) == 2 #We found 2 documents

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_document_project_false(docuement_multi_with_filter):
  BASE_URL = environ.get('API_BASE_URL')

  body =  {"cat_name":"Boone"}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{docuement_multi_with_filter['pack_name']}/data_collection/{docuement_multi_with_filter['data_collection_name']}/document?filter_name={docuement_multi_with_filter['filter_name']}&project=false", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)

  doc_count = loads(response.read().decode('utf-8'))
 
  assert response.getcode() == 200 and len(doc_count) == 1 #We found 1 document


@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_document_with_project_no_match(docuement_multi_with_filter):
  BASE_URL = environ.get('API_BASE_URL')

  body =  {"cat_name":"Axel"}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{docuement_multi_with_filter['pack_name']}/data_collection/{docuement_multi_with_filter['data_collection_name']}/document?filter_name={docuement_multi_with_filter['filter_name']}&project=true", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 204 #No documents found

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_document_var_dont_match(docuement_multi_with_filter):
  BASE_URL = environ.get('API_BASE_URL')

  body =  {"age":7}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{docuement_multi_with_filter['pack_name']}/data_collection/{docuement_multi_with_filter['data_collection_name']}/document?filter_name={docuement_multi_with_filter['filter_name']}&project=true", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 400 #Make sure we got a 400
@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_document_with_project_filter_not_exist(docuement_multi_with_filter):
  BASE_URL = environ.get('API_BASE_URL')

  body =  {"cat_name":"Boone"}
  filter_name = ''.join(random.choices(string.ascii_letters,k=10))

  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{docuement_multi_with_filter['pack_name']}/data_collection/{docuement_multi_with_filter['data_collection_name']}/document?filter_name={filter_name}&project=true", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
  
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 404 #Make sure we got a 404


@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_document_data_collection_does_not_exist():
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = "blarf"
  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))
  filter_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = {}

  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}/document?filter_name={filter_name}&project=true", data=data, method='POST')
  req.add_header("Content-Type", "application/json")
  
  error_code = None
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code =  e.code 

  assert error_code == 404 #Make sure we got a 404

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_document_no_content_type():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  data_collection_name = "asdf"
  filter_name = "asdf"
  body = {}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}/document?filter_name={filter_name}&project=true", data=data, method='POST')

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a media type not supported here
  assert error_code == 415

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_document_content_type_xml():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = "blarf"
  data_collection_name = "asdf"
  filter_name = "asdf"
  body = {}
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}/document?filter_name={filter_name}&project=true", data=data, method='POST')
  req.add_header("Content-Type", "application/xml")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a media type not supported here
  assert error_code == 415

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_post_document_dirty_input():
  BASE_URL = environ.get('API_BASE_URL')

  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))
  filter_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"
  body =  {"$.bad":"nicetry"}
  
  data= dumps(body).encode("utf-8")
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}/document?filter_name={filter_name}&project=true", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get a unprocessable entity when the definition includes a charcter that could indicate an injection attack
  assert error_code == 422

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_pist_document_invalid_json():
  BASE_URL = environ.get('API_BASE_URL')
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  data_collection_name = ''.join(random.choices(string.ascii_letters,k=10))
  filter_name = ''.join(random.choices(string.ascii_letters,k=10))
  body = '{"a"}'
  
  data= body.encode("utf-8")
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection/{data_collection_name}/document?filter_name={filter_name}&project=true", data=data, method='POST')
  req.add_header("Content-Type", "application/json")

  error_code = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_code = e.code 
       
  #We should get an error when the definition includes invalid json
  assert error_code == 400