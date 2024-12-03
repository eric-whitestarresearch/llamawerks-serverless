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
from json import loads
from json.decoder import JSONDecodeError
import re

def prepare_body(func):
  """
  Decorator to sanitize the serivce component definition

  Parameters:
    func(Function): The function you want to execute

  Returns
    The response of the function input is clear, otherwise a HTTP 422
  """

  def wrapper(*args, **kwargs):
    
    event = kwargs['event'] if 'event' in kwargs else args[0]
    context = kwargs['context'] if 'context' in kwargs else args[1]
    regex = '[$.()]'

    if re.search(regex, event['body']):
      return api_gw_response(422, "Definition invalid")
    else:
      try:
        event['body'] = loads(event['body'])
      except JSONDecodeError:
        return api_gw_response(400, "Invalid JSON in request body")
      return func(event=event, context=context)
    
  return wrapper