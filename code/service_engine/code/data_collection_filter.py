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

from modules.datacollectionfilter import DataCollectionFilter
from modules.database import Database

def get_data_collection_filter(event,context):
  """
  Reurns the definition of the data collection filter(s)

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection
  
  Returns:
    Dict: Key: id value: the id of the new data collection
    Int: HTTP status code
  """
  
  dcf = DataCollectionFilter(Database())

  pack_name = event['pathParameters']['pack_name']
  filter_name = None
  if event['queryStringParameters']:
    if 'data_collection_name' in event['queryStringParameters']:
      data_collection_name = event['queryStringParameters']['filter_name']    
  
  return dcf.get_data_collection_filters(pack_name, filter_name)



def create_data_collection_filter(event, context):
  """
  Creates a new data collection filter

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection
  
  Returns:
    Dict: Key: id value: the id of the new data collection
    Int: HTTP status code
  """
  dcf = DataCollectionFilter(Database())

  pack_name = event['pathParameters']['pack_name']
  data_collection_filter_definition = event['body']

  return dcf.create_data_collection_filter(pack_name,data_collection_filter_definition)

def update_data_collection_filter(event, context):
  """
  Updates a data collection_filter

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection
  
  Returns:
    Dict: Key: id value: the id of the new data collection
    Int: HTTP status code
  """
  
  dcf = DataCollectionFilter(Database())

  pack_name = event['pathParameters']['pack_name']
  data_collection_filter_definition = event['body']

  return dcf.update_data_collection_filter(pack_name,data_collection_filter_definition)

def delete_data_collection_filter(event, context):
  """
  Deletes a data collection filter

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection
  
  Returns:
    Dict: Key: id value: the id of the new data collection
    Int: HTTP status code
  """
  
  dcf = DataCollectionFilter(Database())

  pack_name = event['pathParameters']['pack_name']
  filter_name = event['pathParameters']['filter_name']

  return dcf.delete_data_collection_filter(pack_name, filter_name)