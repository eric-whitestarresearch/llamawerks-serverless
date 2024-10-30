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

import boto3

def get(name):
  """
  Gets the SSM Parameter and returns it

  Parameters:
    name (String): The name of the SSM Parameter

  Returns:
    Dict: A dict with the SSM Parameter responce
  
  """

  ssm_client = boto3.client('ssm')

  #If the parameter does not exist or we don't have permissions to it, just halt and catch fire. 
  #This isn't important enough for error handling
  response = ssm_client.get_parameters(Names=[name])

  return {"Parameter": response['Parameters'][0]}