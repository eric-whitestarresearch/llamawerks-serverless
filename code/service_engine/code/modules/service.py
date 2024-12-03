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
from .serviceexecution import ServiceExecution
from .apigwresponse import api_gw_response

class Service(ServiceComponent):
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

  db_collection = "__system.service"
  component_type = "service"
  component_type_name = "service"

  def get_services(self, pack_name, service_name = None):
    """
    Retrieve the service definition from the database

    Parameters:
      pack_name (String): The name of the pack the service(s) is in
      service_name (String): The name of the service (Optional)

    Returns:
      List: A list of dictonaries that contain the service definition(s)
      Int: HTTP status code
    """

    return self.get_service_component(pack_name, service_name)
  
  def delete_service(self, pack_name, service_name):
    """
    Deletes a service

    Parameters:
      pack_name (String): The name of the pack the service is in
      service_name (String): The name of the service to delete

    Returns:
      Dict: Key: deleted value: a count of the services deleted
      Int: HTTP status code
    """

    return self.delete_service_component(pack_name, service_name)

  
  def create_service(self,pack_name,service_definition):
    """
    Creates a new service

    Parameters:
      pack_name (String): The name of the pack to create the service in
      data_collection_definition (Dict): The definition of the service
    
    Returns:
      Dict: Key: id value: the id of the new service
      Int: HTTP status code
    """

    return self.create_service_component(pack_name, service_definition)  

  def update_service(self,pack_name,service_definition):
    """
    Updates a service definition

    Parameters:
      pack_name (String): The name of the pack the service is in
      service_definition (Dict): The definition of the service
    
    Returns:
      Dict: Key: updated, value: a count of the updated service
      Int: HTTP status code
    """

    return self.update_serivce_component(pack_name, service_definition)
  
  def render_service(self, pack_name, service_name):
    """
    Retrieve the data for all fields used in a service

    Parameters:
      pack_name (String): The name of the pack the service(s) is in
      service_name (String): The name of the service (Optional)

    Returns:
      List: A list of dictonaries containing the field used in the service
      Int: HTTP status code
    """

    service_definition = self.get_service_component(pack_name, service_name, encode=False)
    
    try:
      assert service_definition['statusCode'] == 200
    except AssertionError:
      if service_definition['statusCode'] == 404:
        return service_definition #We got a 404 back so just return it up
      else:
        return api_gw_response(400, "Could not render service")
    
    document = DataCollectionDocument(self.db_client)

    result = []
    for field in service_definition['body'][0]['fields']:
      result_field = {
        "name": field['name'],
        "display_name": field['display_name'],
        "display_type": field['display_type'],
        "selection_key": field['selection_key']
      }

      if not field['wait_to_render']:
        field_docs = document.get_document_with_filter(pack_name=pack_name, 
                                                      data_collection_name=field['data_collection'],
                                                      filter_name=field['filter'],
                                                      filter_variables={},
                                                      project=True,
                                                      encode=False)
        try:
          assert field_docs['statusCode'] == 200
        except AssertionError:
          if field_docs['statusCode'] == 404:
            message = "Could not find data collection collection filter"
          else:
            message = "No documents match the data collection filter"
          return api_gw_response(400, message)
        result_field['values'] = field_docs['body']
      else:
        result_field['values'] = None
      result.append(result_field)

    return api_gw_response(200, result_field)
  
  def render_service_field(self, pack_name, service_name, field_name, variables):
    """
    Retreive the data for a field used in a service

    Parameters:
      pack_name (String): The name of the pack the service(s) is in
      service_name (String): The name of the service (Optional)

    Returns:
      List: A list of dictonaries containing the field used in the service
      Int: HTTP status code
    """

    service_definition = self.get_service_component(pack_name, service_name, encode=False)
    
    try:
      assert service_definition['statusCode'] == 200
    except AssertionError:
      if service_definition['statusCode'] == 404:
        return service_definition #We got a 404 back so just return it up
      else:
        return api_gw_response(400, "Could not render service")
    
    document = DataCollectionDocument(self.db_client)

    target_field = None
    for field in service_definition['body'][0]['fields']:
      if field['name'] == field_name:
        target_field = field
        break

    try:
      assert target_field != None
    except AssertionError:
      return api_gw_response(404, f"Could not find field {field_name} in service {service_name}")

    field_docs = document.get_document_with_filter(pack_name=pack_name, 
                                                      data_collection_name=field['data_collection'],
                                                      filter_name=field['filter'],
                                                      filter_variables=variables,
                                                      project=True,
                                                      encode=False)
    try:
      assert field_docs['statusCode'] in [200,204]
    except AssertionError:
      if field_docs['statusCode'] == 404:
        message = "Could not find data collection collection filter"
        return api_gw_response(404, message)
      else:
        message = "Could rend the service field"
        return api_gw_response(400, message)
    
    return field_docs
  
  def execute_service(self, pack_name, service_name, service_vars):
    """
    Retreive the data for a field used in a service

    Parameters:
      pack_name (String): The name of the pack the service(s) is in
      service_name (String): The name of the service (Optional)
      servies_vars (Dict): A dictonary of the variables for the service

    Returns:
      List: A list of dictonaries containing the field used in the service
      Int: HTTP status code
    """

    service_definition = self.get_service_component(pack_name, service_name, encode=False)
    
    try:
      assert service_definition['statusCode'] == 200
    except AssertionError:
      if service_definition['statusCode'] == 404:
        return service_definition #We got a 404 back so just return it up
      else:
        return api_gw_response(400, "Could not execute service")
      
    try:
      assert set(service_vars.keys()) == {i['name'] for i in service_definition['body'][0]['fields']}
    except AssertionError:
      return api_gw_response(400, "Variables in the execution request did not match those in the serivce definition")
    
    se = ServiceExecution(self.db_client)

    return se.submit_service_execution(pack_name, service_name, service_vars)
    