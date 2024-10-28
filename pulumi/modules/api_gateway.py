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

from pulumi import ResourceOptions
from pulumi_aws import apigateway, iam
import pulumi_aws as aws
from time import sleep

class MISSINGENDPOINTEXCEPTION(BaseException):
  pass

def gen_resource_policy(execution_arn, environment, vpc_id):
    """
    Generate the resource policy used by a private REST API

    Parameters:
      execution_arn (String): The execution ARN of the API Gateway
      environment (String): dev, stage, prod, etc
      vpc_id (String): The ID of the vpc allowed to access the api gateway. 
    """
    resource_policy = iam.get_policy_document_output(statements=[
      {
        "effect": "Deny",
        "principals": [{
          "type": "AWS",
          "identifiers": ["*"]
        }],
        "actions": ["execute-api:Invoke"],
        "resources": [f"{execution_arn}/{environment}/*/*"],
        "conditions": [{
            "test" : "StringNotEquals",
            "variable" : "aws:sourceVpc",
            "values": [f"{vpc_id}"]
          }]
      },
      {
        "effect": "Allow",
        "principals": [{
          "type": "AWS",
          "identifiers": ["*"]
        }],
        "actions": ["execute-api:Invoke"],
        "resources": [f"{execution_arn}/{environment}/*/*"]
      }
    ])

    return resource_policy

def api_gateway(name, openai_spec_path, description, environment, vpc_id, private=True, endpoint_ids=[]):
  """
  Create an API Gateway

  Parameters:
    name (String): The name of the API gateway
    openapi_spec_path (String): The path to the openapi spec for the REST API
    description (String): A description of the gateway
    environment (String): dev,stage, prod, etc
    vpc_id (String): The VPC to allow access from
    private (Bool): Is this a private or regional gateway. If private then endpoint_ids must be specified
    endpoint_ids (List): A list of the endpoint IDs to associate the private gateways with.
  """

  if private and len(endpoint_ids) == 0:
    raise MISSINGENDPOINTEXCEPTION("If using a private API Gateway must specify the IDs of the VPC Endpoint")
  
  if private:
     endpoint_config = {
        "types": "PRIVATE",
        "vpcEndpointIds": endpoint_ids
     }

     
  else:
     endpoint_config = {
        "type" : "REGIONAL"
     }
  
  
  with open(openai_spec_path,'r') as file:
      OPENAPI_SPEC =  file.read()

  tags = {
     "Name" : f"{name}",
     "managed_by" : "pulumi"
  }

  rest_api_gw = apigateway.RestApi(name,
                                   description=description,
                                   body=OPENAPI_SPEC,
                                   endpoint_configuration=endpoint_config,
                                   tags=tags)
  
  if private:
    resource_policy = rest_api_gw.execution_arn.apply(lambda arn: gen_resource_policy(arn, environment, vpc_id))

    rest_api_gw_policy = apigateway.RestApiPolicy(f"{name}-{environment}-policy",
                                                  rest_api_id=rest_api_gw.id,
                                                  policy=resource_policy.json)
    deployment_opts = ResourceOptions(depends_on=[rest_api_gw_policy])
  else:
    deployment_opts = None

  deployment = apigateway.Deployment(f"{name}-{environment}",
                                     rest_api=rest_api_gw.id,
                                     description=f"{environment} deployment",
                                     stage_name=environment,
                                     opts=deployment_opts)