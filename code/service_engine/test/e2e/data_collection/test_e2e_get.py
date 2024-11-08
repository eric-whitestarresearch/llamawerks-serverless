import urllib.request
from os import environ
import pytest

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_data_collection():
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = "blarf"
  data_collection_name = "blarf"
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection?data_collection_name={data_collection_name}")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_all_data_collection():
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = "blarf"
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_get_data_collection_does_not_exist():
  BASE_URL = environ.get('API_BASE_URL')

  pack_name = "blarf"
  data_collection_name = "poiuasdf123"
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection?data_collection_name={data_collection_name}")
  response = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    if e.code == 404:
      assert True
    else:
      #We got an error, but it is not a 404 as expected
      assert False
  
  #If we have a response that means we got data back, which is not expected here
  if response != None:
    assert False
@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_get_data_collection_none_in_pack():
  BASE_URL = environ.get('API_BASE_URL')
  
  pack_name = "lkjhoiu"
  
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection")
  response = urllib.request.urlopen(req)

  assert response.getcode() == 204


