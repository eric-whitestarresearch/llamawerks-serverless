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
def test_e2e_render_service(service_renderable):
  BASE_URL = environ.get('API_BASE_URL')

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{service_renderable['pack_name']}/service/{service_renderable['name']}")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200 #It exists

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_render_can_not_render(service_renderable):
  BASE_URL = environ.get('API_BASE_URL')

  #Delete the documents, so the serivce will have no data to render
  for document in service_renderable['documents']:
    req = urllib.request.Request(f"{BASE_URL}/service_engine/{service_renderable['pack_name']}/data_collection/{service_renderable['dc_name']}/document/id/{document['doc_id']}", method='DELETE')
    response = urllib.request.urlopen(req) #Delete the document
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{service_renderable['pack_name']}/service/{service_renderable['name']}")
  
  error_code = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
      error_code = e.code 

  assert error_code == 400 #Make sure we got a 400

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_render_service_does_not_exist():
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = "blarf"
  service_name = ''.join(random.choices(string.ascii_letters,k=10))
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/service/{service_name}")
  
  error_code = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
      error_code = e.code 

  assert error_code == 404 #Make sure we got a 404



  