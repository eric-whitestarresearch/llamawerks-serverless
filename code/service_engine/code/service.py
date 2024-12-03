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

from modules.service import Service
from modules.database import Database
from modules.apigwresponse import api_gw_response
from modules.checkcontenttype import check_content_type
from modules.preparebody import prepare_body
from json import loads
from json.decoder import JSONDecodeError
import logging
import modules.logger

def apigw_handler_service(event, context):
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
      return delete_service(event, context)
    case 'GET':
      return get_services(event, context)
    case 'PATCH':
      return update_service(event, context)
    case 'PUT':
      return create_service(event, context)
    case _:
      raise NotImplementedError(f"Handler for endpoint {event['resource']} method {event['httpMethod']} not implemented")
    
def apigw_handler_service_name(event, context):
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
      return render_service(event, context)
    case 'POST':
      return execute_service(event, context)
    case _:
      raise NotImplementedError(f"Handler for endpoint {event['resource']} method {event['httpMethod']} not implemented")

def apigw_handler_service_field(event, context):
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
      return render_service_field(event, context)
    case _:
      raise NotImplementedError(f"Handler for endpoint {event['resource']} method {event['httpMethod']} not implemented")

def get_services(event, context):
  """
  Reurns the definition of the service(s)

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  
  logging.info("Starting get_services")
  logging.debug(f"request event: {event}")

  service = Service(Database())

  pack_name = event['pathParameters']['pack_name']
  service_name = None
  
  if event['queryStringParameters'] and 'service_name' in event['queryStringParameters']:
    service_name = event['queryStringParameters']['service_name']    
  
  return service.get_services(pack_name, service_name)
  
def delete_service(event, context):
  """
  Deletes a service

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  
  logging.info("Starting delete_service")
  logging.debug(f"request event: {event}")

  service = Service(Database())

  pack_name = event['pathParameters']['pack_name']
  service_name = event['queryStringParameters']['service_name']    

  return service.delete_service(pack_name, service_name)

@check_content_type
@prepare_body
def create_service(event, context):
  """
  Creates a new service

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """

  logging.info("Starting create_service")
  logging.debug(f"request event: {event}")

  service = Service(Database())

  pack_name = event['pathParameters']['pack_name']
  service_definition = event['body']

  return service.create_service(pack_name,service_definition)

@check_content_type
@prepare_body
def update_service(event, context):
  """
  Updates a service

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  
  logging.info("Starting update_service")
  logging.debug(f"request event: {event}")

  service = Service(Database())

  pack_name = event['pathParameters']['pack_name']
  service_definition = event['body']

  return service.update_service(pack_name,service_definition)

def render_service(event, context):
  """
  Reurns the definition of the service(s)

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  
  logging.info("Starting render_service")
  logging.debug(f"request event: {event}")

  service = Service(Database())

  pack_name = event['pathParameters']['pack_name']
  service_name = event['pathParameters']['service_name']
  
  return service.render_service(pack_name, service_name)
@check_content_type
@prepare_body
def render_service_field(event, context):
  """
  Reurns the definition of the service(s)

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  
  logging.info("Starting get_services")
  logging.debug(f"request event: {event}")

  service = Service(Database())

  pack_name = event['pathParameters']['pack_name']
  service_name = event['pathParameters']['service_name']
  field_name = event['pathParameters']['field_name']
  filter_vars = event['body']

  return service.render_service_field(pack_name, service_name, field_name,filter_vars)

@check_content_type
@prepare_body
def execute_service(event, context):
  """
  Reurns the definition of the service(s)

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  
  logging.info("Starting get_services")
  logging.debug(f"request event: {event}")

  service = Service(Database())

  pack_name = event['pathParameters']['pack_name']
  service_name = event['pathParameters']['service_name']
  service_vars = event['body']

  return service.execute_service(pack_name, service_name, service_vars)

