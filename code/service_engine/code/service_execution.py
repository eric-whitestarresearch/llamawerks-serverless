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