import urllib.parse
import urllib.request
from os import environ
import pytest
from json import dumps
import random
import string

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_data_collection():
  BASE_URL = environ.get('API_BASE_URL')
  dc_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"
  body = {
    "name": dc_name,
    "pack": "blarf",
    "fields": [
      {
        "name": "name",
        "type": "string",
        "required": True,
        "index": True,
        "unique": True
      }
    ]
  }
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = urllib.request.urlopen(req)

  assert response.getcode() == 201 #Successfully created

  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection?data_collection_name={dc_name}", method='DELETE')
  response = urllib.request.urlopen(req)

  assert response.getcode() == 200 #Deleted

# @pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
# def test_e2e_put_data_collection_exists():
#   BASE_URL = environ.get('API_BASE_URL')
#   dc_name = ''.join(random.choices(string.ascii_letters,k=10))
#   pack_name = "blarf"
#   body = {
#     "name": dc_name,
#     "pack": "blarf",
#     "fields": [
#       {
#         "name": "name",
#         "type": "string",
#         "required": True,
#         "index": True,
#         "unique": True
#       }
#     ]
#   }
 
#   data= dumps(body).encode("utf-8")
#   req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection", data=data, method='PUT')
#   req.add_header("Content-Type", "application/json")

#   response = urllib.request.urlopen(req)

#   assert response.getcode() == 201 #Successfully created

#   req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection", data=data, method='PUT')
#   req.add_header("Content-Type", "application/json")
#   response = urllib.request.urlopen(req)

#   assert response.getcode() == 200 #Already exists

#   req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection?data_collection_name={dc_name}", method='DELETE')
#   req.add_header("Content-Type", "application/json")
#   response = urllib.request.urlopen(req)

#   assert response.getcode() == 200 #Deleted

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_data_collection_bad_schema():
  BASE_URL = environ.get('API_BASE_URL')
  dc_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"
  body = {
    "name2": dc_name,
    "pack": "blarf",
    "fields": [
      {
        "name": "name",
        "type": "string",
        "required": True,
        "index": True,
        "unique": True
      }
    ]
  }
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection", data=data, method='PUT')
  req.add_header("Content-Type", "application/json")

  response = None

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    if e.code == 400:
      assert True #We expect this when the body does not match schema requirements
    else:
      #We got an error, but it is not a 400 as expected
      assert False
  
  #If we have a response that means we got data back, which is not expected here
  if response != None:
    assert False

@pytest.mark.skipif(environ.get('API_BASE_URL') == None, reason="e2e not enabled")
def test_e2e_put_data_collection_no_content_type():
  BASE_URL = environ.get('API_BASE_URL')
  dc_name = ''.join(random.choices(string.ascii_letters,k=10))
  pack_name = "blarf"
  body = {
    "name2": dc_name,
    "pack": "blarf",
    "fields": [
      {
        "name": "name",
        "type": "string",
        "required": True,
        "index": True,
        "unique": True
      }
    ]
  }
 
  data= bytes(dumps(body).encode("utf-8"))
  req = urllib.request.Request(f"{BASE_URL}/service_engine/{pack_name}/data_collection", data=data, method='PUT')

  response = None
  
  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    if e.code == 415:
      assert True #We expect this when the content type header is not set
    else:
      #We got an error, but it is not a 400 as expected
      assert False
  
  #If we have a response that means we got data back, which is not expected here
  if response != None:
    assert False