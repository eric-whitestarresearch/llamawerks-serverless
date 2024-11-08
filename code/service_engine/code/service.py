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


def get_services(event, context):
  """
  Reurns the definition of the service(s)

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  
  service = Service(Database())

  pack_name = event['pathParameters']['pack_name']
  service_name = None
  if event['queryStringParameters']:
    if 'data_collection_name' in event['queryStringParameters']:
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
  
  service = Service(Database())

  pack_name = event['pathParameters']['pack_name']
  service_name = event['queryStringParameters']['service_name']    

  return service.delete_service(pack_name, service_name)

def create_service(event, context):
  """
  Creates a new service

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  service = Service(Database())

  pack_name = event['pathParameters']['pack_name']
  service_definition = event['body']

  return service.create_service(pack_name,service_definition)

def update_service(event, context):
  """
  Updates a service

  Parameters:
    event (Dict): The event from the API Gateway
    context (Dict): A dict with the contect of the lambda event

  Returns:
    Dict: A dictonary with the response data for API Gateway.
  """
  
  service = Service(Database())

  pack_name = event['pathParameters']['pack_name']
  service_definition = event['body']

  return service.update_service(pack_name,service_definition)