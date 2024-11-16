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
def test_e2e_get_data_collection_filter(data_collection_filter_single):
  BASE_URL = environ.get('API_BASE_URL')

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{data_collection_filter_single['pack_name']}/filter?filter_name={data_collection_filter_single['name']}")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200 #It exists

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_all_data_collection_filter(data_collection_filter_multi):
  BASE_URL = environ.get('API_BASE_URL')
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{data_collection_filter_multi[0]['pack_name']}/filter")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200 #It exists

  dc_count = len(loads(response.read().decode('utf-8')))

  assert dc_count == len(data_collection_filter_multi) 

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_data_collection_filter_does_not_exist():
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = 'blarf'
  filter_name = ''.join(random.choices(string.ascii_letters,k=10))
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter?filter_name={filter_name}")
  response = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    assert e.code == 404 #Make sure we got a 404

  #If we have a response that means we got data back, which is not expected here
  assert response == None

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_get_data_collection_filter_none_in_pack():
  BASE_URL = environ.get('API_BASE_URL')
  
  pack_name = ''.join(random.choices(string.ascii_letters,k=10))
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/filter")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 204