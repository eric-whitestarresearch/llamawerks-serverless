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

from modules.datacollection import DataCollection
from modules.database import Database
from modules.apigwresponse import api_gw_response
from json import loads
import logging
import modules.logger




def get_data_collections(event, context):
  """
  Reurns the definition of the data collections

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  logging.info("Starting get_data_collections")
  logging.debug(f"request event: {event}")

  dc = DataCollection(Database())
  
  pack_name = event['pathParameters']['pack_name']
  data_collection_name = None

  if event['queryStringParameters'] and 'data_collection_name' in event['queryStringParameters']:
    data_collection_name = event['queryStringParameters']['data_collection_name']    

  return dc.get_data_collections(pack_name, data_collection_name)
  
def delete_data_collection(event, context):
  """
  Deletes a data collection

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  
  logging.info("Starting delete_data_collection")
  logging.debug(f"request event: {event}")

  dc = DataCollection(Database())

  pack_name = event['pathParameters']['pack_name']
  data_collection_name = event['queryStringParameters']['data_collection_name']

  return dc.delete_data_collection(pack_name, data_collection_name)

def create_data_collection(event, context):
  """
  Creates a new data collection

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection
  
  Returns:
    Dict: Key: id value: the id of the new data collection
    Int: HTTP status code
  """
  
  logging.info("Starting create_data_collection")
  logging.debug(f"request event: {event}")

  if not 'Content-Type' in event['headers'] or event['headers']['Content-Type'] != 'application/json':
    return api_gw_response(415, "Content type must be application/json")

  dc = DataCollection(Database())
  
  pack_name = event['pathParameters']['pack_name']
  data_collection_definition = loads(event['body'])
  

  return dc.create_data_collection(pack_name,data_collection_definition)

def update_data_collection(event, context):
  """
  Updates a data collection

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection
  
  Returns:
    Dict: Key: updated, value: a count of the updated data collection
    Int: HTTP status code
  """
  
  logging.info("Starting update_data_collection")
  logging.debug(f"request event: {event}")

  if not 'Content-Type' in event['headers'] or event['headers']['Content-Type'] != 'application/json':
    return api_gw_response(415, "Content type must be application/json")

  dc = DataCollection(Database())

  pack_name = event['pathParameters']['pack_name']
  data_collection_definition = loads(event['body'])

  return dc.update_data_collection(pack_name,data_collection_definition)