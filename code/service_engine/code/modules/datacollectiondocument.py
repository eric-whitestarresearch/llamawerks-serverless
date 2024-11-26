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

from .datacollectionfilter import DataCollectionFilter
from .datacollection import DataCollection
from .apigwresponse import api_gw_response

from ast import literal_eval
from bson.objectid import ObjectId
from json import loads

class FilterNotFoundExection(BaseException):
  pass

class DataCollectionDocument():
  """
  Then class for interacting with Data Collection Documents

  Attributes:
    db_client (Database): An instance of the Database class used to interact with the database
    dcf (DataCollectionFilter): An instance of the DataCollectionFilter class used to interact with data collection filters
    dc (DataCollection): An instance of the DataCollection class used to interact with data collections
  
  """

  db_client = None
  dcf = None
  dc =  None

  def __init__(self,db_client):
    """
    The constructor for the DataCollectionDocument class.

    Parameters:
      self (ServiceItem): The object itself
      db_client (Str): A Database object that hosts the connection to the database

    Returns:
      None
    """

    self.db_client = db_client
    self.dcf =  DataCollectionFilter(self.db_client)
    self.dc = DataCollection(self.db_client)

  def check_data_collection_exists(func):
    """
    Decorator to check if a data collection exists, return a 404 if it does not

    Parameters:
      func(Function): The function you want to execute

    Returns
      Function response if the data collection exists, otherwise a 404 response
    """

    def wrapper(*args, **kwargs):
      
      self = kwargs['self'] if 'self' in kwargs else args[0]
      pack_name =   kwargs['pack_name'] if 'pack_name' in kwargs else args[1]
      data_collection_name =   kwargs['data_collection_name'] if 'pack_name' in kwargs else args[2]

      if not self.dc.data_collection_exist(pack_name,data_collection_name):
        return api_gw_response(404, f"The data collection {data_collection_name}, does not exist in pack {pack_name}")  
      else:
        return func(*args, **kwargs)
    return wrapper
  
  @check_data_collection_exists
  def get_documents(self, pack_name, data_collection_name):
    """
    Returns all documents in data collection

    Parameters:
      pack_name (Str): The name of the pack the data collection is in
      data_collection_name (Str): The name of the data collection that contains the document

    Returns:
      Dict: A dictonary containing the documents
      Int: HTTP status code
    """ 

    db_collection = f"{pack_name}.{data_collection_name}"

    db_filter = {}
    documents = self.db_client.find_all_in_collection(db_collection,db_filter)

    if len(documents) > 0:
      return api_gw_response(200, documents)
    else:
      return api_gw_response(204, documents)
  
  @check_data_collection_exists
  def get_document_with_filter(self, pack_name, data_collection_name, filter_name, filter_variables, project, encode=True):
    """
    Returns documents that match a data collection filter

    Parameters:
      pack_name (Str): The name of the pack the data collection is in
      data_collection_name (Str): The name of the data collection that contains the document
      filter_name (Str): The name of the data collection filter
      filter_vriables (Dict): A dictonary containing the values for the variables used by the filter.
                              Key is the name of the variable. Value is the value fo the variable
      project (Boolean): Return all fields or only fields defined in filter projection
      encode (Boolean): Should response body be encoded as string for return to API Gateway

    Returns
      Dict: A dictonary containing the documents
      Int: HTTP status code

    """
    
    db_collection = f"{pack_name}.{data_collection_name}"

    try:
      gen_filter_result = self.generate_db_filter_projection(pack_name, filter_name, filter_variables, gen_projection=project)
    except FilterNotFoundExection:
      return api_gw_response(404, f"filter: {filter_name} not found in pack: {pack_name}")
    except AssertionError:
      return api_gw_response(400, f"variables in request do not match that of the filter definition")

    db_filter = gen_filter_result[0]
    db_projection = gen_filter_result[1]
    
    documents = self.db_client.find_all_in_collection(db_collection,db_filter, db_projection)

    if len(documents) > 0:
      return api_gw_response(200, documents, encode=encode)
    else:
      return api_gw_response(204, documents)
  
  def generate_db_filter_projection(self, pack_name, filter_name, filter_variables, gen_projection = False):
    """
    Generates the the filter used by the database from a data collection filter
    Will apply the variables so it is in a form useable by the database

    Parameters:
      pack_name (Str): The name of the pack the data collection is in
      data_collection_name (Str): The name of the data collection that contains the document
      filter_name (Str): The name of the data collection filter
      filter_vriables (Dict): A dictonary containing the values for the variables used by the filter.
                              Key is the name of the variable. Value is the value fo the variable

    Returns
      Dict: A mongo database filter

    """
    #If the filter is not found the request will abort with a 404
    result = self.dcf.get_data_collection_filters(pack_name,filter_name)
    
    if result['statusCode'] in [204, 404]:
      raise FilterNotFoundExection(f"filter: {filter_name} not found in pack {pack_name}")
    
    result_body = loads(result['body'])[0]

    db_filter = result_body['filter']
    db_filter_string = str(db_filter)
    variables = result_body['variables']
    
    #Before substuting, make sure that list variables given matches what we need.
    assert [i['name'] for i in variables] == list(filter_variables.keys())

    for var in variables:
      string_to_replace = f"#{var['name']}#" if var['type'] == "string" else f"\'#{var['name']}#\'"
      db_filter_string = db_filter_string.replace(string_to_replace, str(filter_variables[var['name']]))
    db_filter = literal_eval(db_filter_string)
    
    if not gen_projection:
      return db_filter, {} 
    else:
      fields = result_body['project']
      projection = {fields[i]: 1 for i in range(0, len(fields))}
      projection['_id'] = 0 
      return db_filter, projection
  
  @check_data_collection_exists
  def create_document(self, pack_name, data_collection_name, document):
    """
    Creates a document in the data collection

    Parameters:
      pack_name (Str): The name of the pack the data collection is in
      data_collection_name (Str): The name of the data collection that contains the document
      document (Dict): The document to add to the database

    Returns:
      Dict: Key: id value: the id of the new document
      Int: HTTP status code

    """
    
    db_collection = f"{pack_name}.{data_collection_name}"
    result = self.db_client.insert_document(db_collection, document)

    return api_gw_response(200, {"id":result})
  
  @check_data_collection_exists
  def update_document(self, pack_name, data_collection_name, filter_name, filter_variables, document_updates):
    """
    Updates documents in the data collection that match a filter

    Parameters:
      pack_name (Str): The name of the pack the data collection is in
      data_collection_name (Str): The name of the data collection that contains the document
      filter_name (Str): The name of the data collection filter
      filter_vriables (Dict): A dictonary containing the values for the variables used by the filter.
                              Key is the name of the variable. Value is the value fo the variable
      document_updates (Dict): A dictonary containing the updates to the document

    Returns:
      Dict: Key: updated, value: a count of the updated documents
      Int: HTTP status code
    
    """
    
    try:
      db_filter = (self.generate_db_filter_projection(pack_name, filter_name, filter_variables, gen_projection=False))[0]
    except FilterNotFoundExection:
      return api_gw_response(404, f"filter: {filter_name} not found in pack: {pack_name}")
    except AssertionError:
      return api_gw_response(400, f"variables in request do not match that of the filter definition")
    
    db_collection = f"{pack_name}.{data_collection_name}"

    result = self.db_client.update_document(db_collection, db_filter, document_updates, upsert=False)

    return api_gw_response(200, {"updated" : result})

  @check_data_collection_exists
  def get_document_by_id(self, pack_name, data_collection_name, document_id):
    """
    Returns document that matches the document id

    Parameters:
      pack_name (Str): The name of the pack the data collection is in
      data_collection_name (Str): The name of the data collection that contains the document
      document_id (Str): The document ID. This is a 24 character hex string that is the _id in the mongo database

    Returns
      Dict: A dictonary containing the documents
      Int: HTTP status code

    """
    
    db_collection = f"{pack_name}.{data_collection_name}"

    db_filter = {"_id": ObjectId(document_id)}
    documents = self.db_client.find_one_in_collection(db_collection,db_filter)

    if not documents:
      return api_gw_response(404, f"A document with id {document_id} not found in data collection {data_collection_name} in pack {pack_name}")
    else:
      return api_gw_response(200, documents)
  
  @check_data_collection_exists
  def update_document_by_id(self, pack_name, data_collection_name, document_id, document):
    """
    Updates document that matches the document id

    Parameters:
      pack_name (Str): The name of the pack the data collection is in
      data_collection_name (Str): The name of the data collection that contains the document
      document_id (Str): The document ID. This is a 24 character hex string that is the _id in the mongo database
      document (Dict): A dictonary containing the updates to the document

    Returns:
      Dict: Key: updated, value: a count of the updated documents
      Int: HTTP status code
    
    """
    
    db_collection = f"{pack_name}.{data_collection_name}"
    db_filter = {"_id": ObjectId(document_id)}

    result = self.db_client.update_document(db_collection, db_filter, document, upsert=False)

    return api_gw_response(200, {"updated" : result})
  
  @check_data_collection_exists
  def delete_document_by_id(self, pack_name, data_collection_name, document_id ):
    """
    Delete document that matches the document id

    Parameters:
      pack_name (Str): The name of the pack the data collection is in
      data_collection_name (Str): The name of the data collection that contains the document
      document_id (Str): The document ID. This is a 24 character hex string that is the _id in the mongo database
    
    Returns:
      Dict: Key: deleted, value: a count of the deleted documents
      Int: HTTP status code
    
    """
    
    db_collection = f"{pack_name}.{data_collection_name}"
    db_filter = {"_id": ObjectId(document_id)}

    result = self.db_client.delete_document(db_collection, db_filter)

    return api_gw_response(200, {"deleted": result})
  