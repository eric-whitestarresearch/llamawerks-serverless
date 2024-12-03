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

from .apigwresponse import api_gw_response
import re

def validate_doc_id(func):
  """
  Decorator to check if the document ID is valid

  Parameters:
    func(Function): The function you want to execute

  Returns
    The response of the function if the content type is correct, otherwise a HTTP 400
  """

  def wrapper(*args, **kwargs):
    
    event = kwargs['event'] if 'event' in kwargs else args[0]
    document_id = event['pathParameters']['document_id'] #API Gateway will enforce the existance of the document id, but it won't validate it
    regex = '^[0-9a-f]{24}$'

    if not re.search(regex, document_id):
      return api_gw_response(400, "Document ID must be 24 hexadecimal lowercase characters")
    else:
      return func(*args, **kwargs)
    
  return wrapper