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


import pulumi
import yaml
import pulumi_aws as aws
from os import environ

from modules.vpc_endpoint import vpc_endpoint
from modules.api_gateway import api_gateway

class MisssingConfigException(BaseException):
  pass

class IncorrectAwsAccountException(BaseException):
  pass

class IncorrectAwsRegionException(BaseException):
  pass

if not environ['LW_IAC_CONFIG']:
  raise MisssingConfigException("Environment variable LW_IAC_CONFIG is not set. Need this to read the config")
else:
    with open(environ['LW_IAC_CONFIG'],'r') as file:
      IAC_CONFIG = yaml.safe_load(file)
    # TO-DO Add validation of the yaml

if IAC_CONFIG['high_availability']:
  subnets = [IAC_CONFIG['vpc']['private_subnet_a'],
             IAC_CONFIG['vpc']['private_subnet_b'],
             IAC_CONFIG['vpc']['private_subnet_c']]
else: 
  subnets = [IAC_CONFIG['vpc']['private_subnet_a']]

if aws.get_caller_identity().account_id != IAC_CONFIG['aws_account_id']:
  raise IncorrectAwsAccountException(f"The wrong AWS account is targeted. Using {aws.get_caller_identity().account_id } expected {IAC_CONFIG['aws_account_id']}")

if aws.get_region().name != IAC_CONFIG['region']:
  raise IncorrectAwsRegionException(f"The wring AWS region is targeted. Using {aws.get_region().name} expected {IAC_CONFIG['region']}")
else:
  region = aws.get_region().name

environment = pulumi.get_stack()


api_gateway_endpoint = vpc_endpoint(f"lw_api_gw_{environment}",
                                    region=region,
                                    service_name='execute-api',
                                    vpc_id=IAC_CONFIG['vpc']['vpc_id'],
                                    subnet_ids=subnets,
                                    )

rest_api_gw = api_gateway(f"lw_api_gw_{environment}",
                          "./openapi.yaml",
                          "The rest api for serverless llamawerks",
                          environment,
                          vpc_id=IAC_CONFIG['vpc']['vpc_id'],
                          private=True,
                          endpoint_ids=[api_gateway_endpoint.id])