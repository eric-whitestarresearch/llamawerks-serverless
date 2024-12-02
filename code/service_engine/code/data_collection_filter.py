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

from modules.datacollectionfilter import DataCollectionFilter
from modules.database import Database
from modules.apigwresponse import api_gw_response
from modules.checkcontenttype import check_content_type
from modules.preparebody import prepare_body
from json import loads
from json.decoder import JSONDecodeError
import logging
import modules.logger

def apigw_handler_filter(event, context):
  """
  Calls the function that handles the HTTP method

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection

  Returns:
    Dict with api gateway response 
  """

  match event['httpMethod']:
    case 'DELETE':
      return delete_data_collection_filter(event, context)
    case 'GET':
      return get_data_collection_filter(event, context)
    case 'PATCH':
      return update_data_collection_filter(event, context)
    case 'PUT':
      return create_data_collection_filter(event, context)
    case _:
      raise NotImplementedError(f"Handler for endpoint {event['resource']} method {event['httpMethod']} not implemented")
    
def get_data_collection_filter(event,context):
  """
  Reurns the definition of the data collection filter(s)

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection
  
  Returns:
    Dict: Key: id value: the id of the new data collection
    Int: HTTP status code
  """

  logging.info("Starting get_data_collection_filter")
  logging.debug(f"request event: {event}")
  
  dcf = DataCollectionFilter(Database())

  pack_name = event['pathParameters']['pack_name']
  filter_name = None
  if event['queryStringParameters'] and 'filter_name' in event['queryStringParameters']:
    filter_name = event['queryStringParameters']['filter_name']    
  
  return dcf.get_data_collection_filters(pack_name, filter_name)


@check_content_type
@prepare_body
def create_data_collection_filter(event, context):
  """
  Creates a new data collection filter

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection
  
  Returns:
    Dict: Key: id value: the id of the new data collection
    Int: HTTP status code
  """

  logging.info("Starting create_data_collection_filter")
  logging.debug(f"request event: {event}")

  dcf = DataCollectionFilter(Database())

  pack_name = event['pathParameters']['pack_name']
  data_collection_filter_definition = event['body']
  
  return dcf.create_data_collection_filter(pack_name,data_collection_filter_definition)

@check_content_type
@prepare_body
def update_data_collection_filter(event, context):
  """
  Updates a data collection_filter

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection
  
  Returns:
    Dict: Key: id value: the id of the new data collection
    Int: HTTP status code
  """
  
  logging.info("Starting update_data_collection_filter")
  logging.debug(f"request event: {event}")

  dcf = DataCollectionFilter(Database())

  pack_name = event['pathParameters']['pack_name']
  data_collection_filter_definition = event['body']
  
  return dcf.update_data_collection_filter(pack_name,data_collection_filter_definition)

def delete_data_collection_filter(event, context):
  """
  Deletes a data collection filter

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection
  
  Returns:
    Dict: Key: id value: the id of the new data collection
    Int: HTTP status code
  """
  
  logging.info("Starting delete_data_collection_filter")
  logging.debug(f"request event: {event}")

  dcf = DataCollectionFilter(Database())

  pack_name = event['pathParameters']['pack_name']
  filter_name = event['queryStringParameters']['filter_name']

  return dcf.delete_data_collection_filter(pack_name, filter_name)