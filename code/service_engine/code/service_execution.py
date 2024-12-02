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

from modules.serviceexecution import ServiceExecution
from modules.database import Database
from modules.checkcontenttype import check_content_type
from modules.preparebody import prepare_body
import logging
import modules.logger


def apigw_handler_execution(event, context):
  """
  Calls the function that handles the HTTP method

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection

  Returns:
    Dict with api gateway response 
  """

  match event['httpMethod']:
    case 'POST':
      return search_service_execution(event,context)
    case _:
      raise NotImplementedError(f"Handler for endpoint {event['resource']} method {event['httpMethod']} not implemented")

def apigw_handler_execution_id(event, context):
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
      return delete_service_execution(event,context)
    case 'GET':
      return get_service_execution(event,context)
    case 'POST':
      return update_service_execution(event,context)
    case _:
      raise NotImplementedError(f"Handler for endpoint {event['resource']} method {event['httpMethod']} not implemented")


def get_service_execution(event, context):
  """
  Returns the context of a service execution

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  
  logging.info("Starting get_service_execution")
  logging.debug(f"request event: {event}")

  se = ServiceExecution(Database())

  document_id =  event['pathParameters']['document_id']
   
  return se.get_service_execution(document_id)

@check_content_type
@prepare_body
def search_service_execution(event, context):
  """
  Searches for service execution using a set of values

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  
  logging.info("Starting get_service_execution")
  logging.debug(f"request event: {event}")

  se = ServiceExecution(Database())
  pack = None
  service_name = None
  document_id = None
  status = None
  before = None
  after = None

  body = event['body']

  if 'document_id' in body:
     document_id = body['document_id']
  if 'status' in body:
    status = body['status']
  if 'pack' in body:
     pack = body['pack']
  if 'service_name' in body:
    service_name = body['service_name']
  if 'before' in body:
    before = body['before']
  if 'after' in body:
    after = body['after']
  if 'fields' in body:
    fields = body['fields']
  

   
  return se.get_service_execution_by_filter(pack = pack,
                                            service_name = service_name,
                                            document_id = document_id,
                                            status = status,
                                            before = before,
                                            after = after,
                                            fields = fields)

@check_content_type
@prepare_body
def update_service_execution(event, context):
  """
  Updates a service execution record

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  
  logging.info("Starting update_service_execution")
  logging.debug(f"request event: {event}")

  se = ServiceExecution(Database())

  document_id =  event['pathParameters']['document_id']
  execution_updates = event['body']
  

  return se.update_service_execution(document_id,execution_updates)

def delete_service_execution(event, context):
  """
  Deletes a service execution

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  
  logging.info("Starting delete_service_execution")
  logging.debug(f"request event: {event}")

  se = ServiceExecution(Database())

  document_id =  event['pathParameters']['document_id']  

  return se.delete_service_execution(document_id=document_id)