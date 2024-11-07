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

from json import dumps

def api_gw_response(status_code, body={}, headers={}):
  """"
  Builds a dictonary needed by AWS API GW to return the proper data to a client

  Parameters:
    status_code (Int): The HTTP Status code
    body (Dict|String): Optional. A dictonary or string with the body of the response
    headers: The HTTP headers to add to the response. The CORS headers are added by default.

  Returns:
    Dicts. A dict with the schema that API Gateway expects
  
  """

  #Add the CORS headers
  #TO-DO. Tighten up CORS. For now just allow everything so we can test.
  headers['Access-Control-Allow-Headers'] = 'Content-Type'
  headers['Access-Control-Allow-Origin'] = '*'
  headers['Access-Control-Allow-Methods'] = '*'


  return {"body": dumps(body), "statusCode": status_code, "headers": headers}


  
  