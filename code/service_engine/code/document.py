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

from modules.datacollectiondocument import DataCollectionDocument
from modules.database import Database
from modules.apigwresponse import api_gw_response
from modules.checkcontenttype import check_content_type
from modules.preparebody import prepare_body
from modules.validiatedocumentid import validate_doc_id
import modules.logger
from json import loads
from json.decoder import JSONDecodeError
import logging



def apigw_handler_document(event, context):
  """
  Calls the function that handles the HTTP method

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection

  Returns:
    Dict with api gateway response 
  """

  match event['httpMethod']:
    case 'GET':
      return get_documents(event, context)
    case 'PATCH':
      return update_document_by_filter(event, context)
    case 'POST':
      return get_document_with_filter(event,context)
    case 'PUT':
      return create_document(event, context)
    case _:
      raise NotImplementedError(f"Handler for endpoint {event['resource']} method {event['httpMethod']} not implemented")
    
def apigw_handler_document_id(event, context):
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
      return delete_document_by_id(event, context)
    case 'GET':
      return get_document_by_id(event, context)
    case 'PATCH':
      return update_document_by_id(event, context)
    case _:
      raise NotImplementedError(f"Handler for endpoint {event['resource']} method {event['httpMethod']} not implemented")
    

def get_documents(event, context):
  """
  Reurns documents in data collection

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """

  logging.info("Starting get_documents")
  logging.debug(f"request event: {event}")

  dcd = DataCollectionDocument(Database())

  pack_name = event['pathParameters']['pack_name']
  data_collection_name = event['pathParameters']['data_collection_name']

  return dcd.get_documents(pack_name, data_collection_name)

@check_content_type
@prepare_body
def get_document_with_filter(event, context):
  """
  Reurns documents matching a filter

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """

  logging.info("Starting get_document_with_filter")
  logging.debug(f"request event: {event}")

  dcd = DataCollectionDocument(Database())

  pack_name = event['pathParameters']['pack_name']
  data_collection_name = event['pathParameters']['data_collection_name']
  filter_name = event['queryStringParameters']['filter_name']   
  project = event['queryStringParameters']['project'] if 'project' in event['queryStringParameters'] else False
  filter_variables = event['body']

  return dcd.get_document_with_filter(pack_name, data_collection_name, filter_name, filter_variables, project)

@check_content_type
@prepare_body
def create_document(event, context):
  """
  Create a new document

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """

  logging.info("Starting create_document")
  logging.debug(f"request event: {event}")

  dcd = DataCollectionDocument(Database())

  pack_name = event['pathParameters']['pack_name']
  data_collection_name = event['pathParameters']['data_collection_name']
  document = event['body']

  return dcd.create_document(pack_name, data_collection_name, document)

@check_content_type
@prepare_body
def update_document_by_filter(event, context):
  """
  Updates a document(s) matching a filter

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """

  logging.info("Starting update_document_by_filter")
  logging.debug(f"request event: {event}")

  dcd = DataCollectionDocument(Database())

  pack_name = event['pathParameters']['pack_name']
  data_collection_name = event['pathParameters']['data_collection_name']
  filter_name = event['queryStringParameters']['filter_name']
  document_and_vars = event['body']

  return dcd.update_document(pack_name, data_collection_name, filter_name, document_and_vars['variables'], document_and_vars['document'])

@validate_doc_id
def get_document_by_id(event, context):
  """
  Get a document by its id

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """

  logging.info("Starting get_document_by_id")
  logging.debug(f"request event: {event}")

  dcd = DataCollectionDocument(Database())

  pack_name = event['pathParameters']['pack_name']
  data_collection_name = event['pathParameters']['data_collection_name']
  document_id = event['pathParameters']['document_id']

  return dcd.get_document_by_id(pack_name, data_collection_name, document_id)

@check_content_type
@validate_doc_id
@prepare_body
def update_document_by_id(event, context):
  """
  Updates a document matching the id

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """

  logging.info("Starting update_document_by_id")
  logging.debug(f"request event: {event}")
  
  dcd = DataCollectionDocument(Database())
  
  pack_name = event['pathParameters']['pack_name']
  data_collection_name = event['pathParameters']['data_collection_name']
  document_id = event['pathParameters']['document_id']
  document = event['body']

  return dcd.update_document_by_id(pack_name, data_collection_name, document_id, document['document'])

@validate_doc_id
def delete_document_by_id(event, context):
  """
  Deletes the document matching the ID.

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """

  logging.info("Starting delete_document_by_id")
  logging.debug(f"request event: {event}")

  dcd = DataCollectionDocument(Database())

  pack_name = event['pathParameters']['pack_name']
  data_collection_name = event['pathParameters']['data_collection_name']
  document_id = event['pathParameters']['document_id']

  return dcd.delete_document_by_id(pack_name, data_collection_name, document_id)