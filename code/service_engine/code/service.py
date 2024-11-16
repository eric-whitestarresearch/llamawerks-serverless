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
from json import loads
import logging
import modules.logger


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
  service_definition = loads(event['body'])

  return service.create_service(pack_name,service_definition)

@check_content_type
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
  service_definition = loads(event['body'])

  return service.update_service(pack_name,service_definition)