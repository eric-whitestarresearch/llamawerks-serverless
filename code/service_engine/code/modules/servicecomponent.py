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
import json
from .apigwresponse import api_gw_response
from bson.objectid import ObjectId
import re

class ServiceComponent:
  """
  The superclass for all service  components i.e. Data Collections, Documents, Filters, Packs, Services
  This class is not meant to be used directly. It should be inherited by child class.

  Attributes:
    db_client (Database): A Database object that hosts the connection to the database
    db_collection (String): The collection in the database for this item type. It will be defined in the child class
    component_type (String): What kind of item this is. It will be defined in the child class.
    component_type_name (String): Display name for this item type. It will be defined in the child class.
  """

  db_client = None
  db_collection = ""
  component_type = ""
  component_type_name = ""

  def __init__(self,db_client) -> None:
    """
    The constructor for the ServiceComponent class.

    Parameters:
      self (ServiceItem): The object itself
      db_client (Str): A Database object that hosts the connection to the database
    """

    self.db_client = db_client

  def service_component_exists(self, pack_name, service_component_name):
    """
    Check if a service component exists

    Parameters:
      pack_name (String): The name of the pack the service item is in
      service_component_name (String): The name of the service component

    Returns:
      Bool: True if exist, false if not
    
    """
    db_filter = {"pack": str(pack_name), "name": str(service_component_name)}
    service_items = [self.db_client.find_all_in_collection(self.db_collection,db_filter)]
    if service_items[0]:
      return True
    else:
      return False

  def get_service_component(self, pack_name, service_component_name = None, encode = True):
    """
    Retrieve the service component from the database

    Parameters:
      pack_name (String): The name of the pack the service item is in
      service_component_name (String): The name of the service component (Optional)
      encode (Boolean): Should the body in the return be dumped to a text string

    Returns:
      List: A list of dictonaries that contain the service component definition(s)
      Int: HTTP status code
    """

    if service_component_name:
      db_filter = {"pack": str(pack_name), "name": str(service_component_name)}
      if not self.service_component_exists(pack_name, service_component_name):
        return api_gw_response(404, f"Could not find {self.component_type_name} {service_component_name} in pack {pack_name}")
    else:
      db_filter = {"pack": str(pack_name)}
      
    service_items = self.db_client.find_all_in_collection(self.db_collection,db_filter)

    if not len(service_items):
      return api_gw_response(204, service_items)  #The pack has no service items
    else: 
      return api_gw_response(200, service_items, encode=encode)
    
  def get_service_component_by_filter(self, filter, projection, encode = True):
    """
    Retrieve the service component from the database

    Parameters:
      filter (Dict): The filter to use when queriring the database
      projection (Dict): A mongo DB projection of the fields to include in the output
      encode (Boolean): Should the body in the return be dumped to a text string

    Returns:
      List: A list of dictonaries that contain the service component definition(s)
      Int: HTTP status code
    """
      
    service_items = self.db_client.find_all_in_collection(self.db_collection,filter, projection)

    if not len(service_items):
      return api_gw_response(404, f"Could not find any {self.component_type_name} that matched the filter")  #The pack has no service items
    else: 
      return api_gw_response(200, service_items, encode=encode)
    
  def delete_service_component(self, pack_name = None, service_component_name = None, document_id = None):
    """
    Deletes a service component

    Parameters:
      pack_name (String): The name of the pack the data collection is in
      service_component_name (String): The name of the service component to delete
      document_id (String): The mongo document id

    Returns:
      Dict: Key: deleted value: a count of the components deleted
      Int: HTTP status code
    """

    try:
      assert (pack_name and service_component_name) or document_id #Make sure with have pack name and component name or a document id
    except AssertionError:
      api_gw_response(400, f"Must have a pack name and {service_component_name} name or a document id")

    if document_id:
      db_filter = {"_id": ObjectId(document_id)}
    else:
      db_filter = {'pack' : str(pack_name), 'name': str(service_component_name)}

    delete_count = self.db_client.delete_document(self.db_collection, db_filter)

    return api_gw_response(200, {"deleted" : delete_count})
  
  def create_service_component(self,pack_name,service_component_definition, is_service_execution=False):
    """
    Creates a new service component

    Parameters:
      pack_name (String): The name of the pack to create the service component in
      service_component_definition (Dict): The definition of the service component
    
    Returns:
      Dict: Key: id value: the id of the new service component
      Int: HTTP status code
    """
    
    try:
      assert pack_name == service_component_definition['pack']
    except AssertionError:
      return api_gw_response(422, f"The pack name specified in the URI and the {self.component_type_name} definition do not match")
    
    if not is_service_execution: #We want to always create an execution
      #Check to see if this service component already exists. If it does, don't create it again.
      filter = {'pack': str(pack_name), 'name': str(service_component_definition['name'])}
      data_collection = self.db_client.find_all_in_collection(self.db_collection, filter)

      if len(data_collection):
        return api_gw_response(200, { "id": data_collection[0]['id'] })
    
    new_service_component_id = self.db_client.insert_document(self.db_collection, service_component_definition)


    return api_gw_response(201, { "id": new_service_component_id })

  def update_serivce_component(self, pack_name, service_component_definition, document_id = None):
    """
    Updates a service component

    Parameters:
      pack_name (String): The name of the pack to update the service component in
      service_component_definition (Dict): The definition of the service component
      id (String): Optional mongodb record ID. A 24 character hex ID.
    
    Returns:
      Dict: Key: updated, value: a count of the updated components
      Int: HTTP status code
    """
    
    #Check to see if this service component already exists. If it does not, stop.
    if document_id:
      filter = {"_id": ObjectId(document_id)}
    else:
      try:
        assert pack_name == service_component_definition['pack']
      except AssertionError:
        return api_gw_response(422, f"The pack name specified in the URI and the {self.component_type_name} definition do not match")
        
      filter = {'pack': str(pack_name), 'name': str(service_component_definition['name'])}

    try:
      assert self.db_client.find_all_in_collection(self.db_collection, filter)
    except AssertionError:
      if not document_id:
        return api_gw_response(404, f"The {self.component_type_name}  {service_component_definition['name']} in pack {pack_name} does not exist. Use put method to create it")
      else:
        return api_gw_response(404, f"The {self.component_type_name}  with id {document_id} does not exist.")

    update_count = self.db_client.update_document(self.db_collection, filter, service_component_definition)

    if update_count:
      return api_gw_response(202, { "updated" : update_count })
    else:
      return api_gw_response(208, { "updated" : 0 })
      




