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

def check_content_type(func):
    """
    Decator to check if the content type is application/json otherwise return a 415

    Parameters:
      func(Function): The function you want to execute

    Returns
      The response of the function if the content type is correct, otherwise a HTTP 415
    """

    def wrapper(*args, **kwargs):
      
      event = kwargs['event'] if 'event' in kwargs else args[0]
      
      if not 'Content-Type' in event['headers'] or event['headers']['Content-Type'] != 'application/json':
        return api_gw_response(415, "Content type must be application/json")
      else:
        return func(*args, **kwargs)
      
    return wrapper