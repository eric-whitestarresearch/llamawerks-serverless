#     Llamawerks - A portal for users to request services with runbook automation
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

from .servicecomponent import ServiceComponent
from .datacollectiondocument import DataCollectionDocument
from .apigwresponse import api_gw_response

from time import time


class ServiceExecution(ServiceComponent):
  """
  The class for interacting with Data Collection Filters

  Attributes:
    item_type (String): What kind of item this is. It will be defined in the child class.
    item_type_name (string): Display name for this item type

  Inherited Attributes:
    db_client (Database): This is defined and set in the parent class
    db_collection (String): The collection in the database for this item type. It will be defined in the child class

  Inherited Methods
    __init__
    get_service_components
    delete_service_component
    create_service_component
    update_serivce_component
  
  """

  db_collection = "__system.service_execution"
  component_type = "service"
  component_type_name = "service execution"

  def get_service_execution(self, document_id):
    """
    Retrieve the service execution context

    Parameters:
      document_id (String): The ID of the mongo document storing the execution context
      
    Returns:
      List: A list of dictonaries that contain the service definition(s)
      Int: HTTP status code
    """

    return self.get_service_component(document_id=document_id)
  
  def delete_service_execution(self, document_id):
    """
    Deletes a service execution

    Parameters:
      document_id (String): The ID of the mongo document storing the execution context

    Returns:
      Dict: Key: deleted value: a count of the services deleted
      Int: HTTP status code
    """

    return self.delete_service_component(document_id=document_id)

  
  def submit_service_execution(self,pack_name, service_name, service_vars):
    """
    Creates a new service execution record

    Parameters:
      pack_name (String): The name of the pack to create the service in
      data_collection_definition (Dict): The definition of the service
    
    Returns:
      Dict: Key: id value: the id of the new service
      Int: HTTP status code
    """

    start_time =int(time())

    execution_definition = {
      "pack" : pack_name,
      "service_name" : service_name,
      "status" : "submitted",
      "submission_time" : start_time,
      "updated_time" : start_time,
      "variables" : service_vars,
      "result" : {}
    }

    return self.create_service_component(pack_name, execution_definition, is_service_execution=True)  

  def update_service_execution(self,document_id,execution_updates):
    """
    Updates a service definition execution

    Parameters:
      pack_name (String): The name of the pack the service is in
      service_definition (Dict): The definition of the service
    
    Returns:
      Dict: Key: updated, value: a count of the updated service
      Int: HTTP status code
    """

    updated_time =int(time())

    document_updates = {
      'updated_time' : updated_time,
      'status' : execution_updates['status'],
      f"result.{execution_updates['result']['step']}" : {
        "output" : execution_updates['result']['output'],
        "error" : execution_updates['result']['error'],
        "status" : execution_updates['result']['status']
      }
    }

    return self.update_serivce_component(pack_name='',
                                        service_component_definition=document_updates,
                                        document_id=document_id)
  