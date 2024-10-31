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

from modules.datacollection import DataCollection
from modules.database import Database


def get_data_collections(event, context):
  """
  Reurns the definition of the data collections

  Parameters:
    pack_name (String): The name of the pack to return the data collections for
    collection_name (String): The name of the data collection to retreive (Optional)

  Returns:
    List: A list of dictonaries that contain the data collection definition(s)
    Int: HTTP status code
  """
  
  dc = DataCollection(Database())
  
  pack_name = event['pathParameters']['pack_name']
  data_collection_name = None
  if event['queryStringParameters']:
    if 'data_collection_name' in event['queryStringParameters']:
      data_collection_name = event['queryStringParameters']['data_collection_name']    

  return dc.get_data_collections(pack_name, data_collection_name)
  
# def delete_data_collection(pack_name, data_collection_name):
#   """
#   Deletes a data collection

#   Parameters:
#     pack_name (String): The name of the pack the data collection is in
#     collection_name (String): The name of the data collection to delete

#   Returns:
#     Dict: Key: deleted value: a count of the data collection deleted
#     Int: HTTP status code
#   """
  
#   dc = DataCollection(request.state.db_client)

#   return dc.delete_data_collection(pack_name, data_collection_name)

# def create_data_collection(pack_name,data_collection_definition):
#   """
#   Creates a new data collection

#   Parameters:
#     pack_name (String): The name of the pack to create the data collections in
#     data_collection_definition (Dict): The definition of the data collection
  
#   Returns:
#     Dict: Key: id value: the id of the new data collection
#     Int: HTTP status code
#   """
#   dc = DataCollection(request.state.db_client)

#   return dc.create_data_collection(pack_name,data_collection_definition)

# def update_data_collection(pack_name, data_collection_definition):
#   """
#   Updates a data collection

#   Parameters:
#     pack_name (String): The name of the pack to create the data collections in
#     data_collection_definition (Dict): The definition of the data collection
  
#   Returns:
#     Dict: Key: updated, value: a count of the updated data collection
#     Int: HTTP status code
#   """
  
#   dc = DataCollection(request.state.db_client)

#   return dc.update_data_collection(pack_name,data_collection_definition)