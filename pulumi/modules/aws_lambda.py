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

import pulumi
import pulumi_aws as aws
from json import dumps

from .aws_lambda_sg import aws_lambda_sg


def aws_lambda(name, package_location, package_checksum_location, handler, subnets, vpc_id, execution_role_arn,
               database, mongodb_host):
  """
  Create a Lambda Function in AWS

  Parameters:
    name (String): The name of the lambda function
    package_location (String): The location of the zip file with the code
    package_checksum_location (String): The location of the file with the checksum for the package
    handler (String): The hander in the code for the lambda function
    subnets (List(string)): A list of subnet ids in the VPC that the lambda should attach to
    vpc_id (String): The VPC ID of the VPC the lambda attaches to
    execution_role_arn (String): The ARN of the execution role for the lambda function
    database (String): The name of the database to connect to
    mongodb_host (String): The hostname of the mongodb database

  Returns:
    None
  """

  with open(package_checksum_location,'r') as sum_file:
    package_checksum = sum_file.readline().rstrip()

  
  code_package = pulumi.FileArchive(package_location)
  
  lambda_environment_vars = {
    "variables" : {
      'MONGODB_DATABASE' : database,
      'MONGODB_HOST' : mongodb_host
    }
  }

  new_lambda = aws.lambda_.Function(name,
    code=code_package,
    name=f"lw_{name}",
    role=execution_role_arn,
    handler=handler,
    source_code_hash=package_checksum,
    runtime=aws.lambda_.Runtime.PYTHON3D12,
    memory_size=2048, #This gets us more CPU
    architectures=["arm64"],
    timeout=5,
    vpc_config={
      "subnet_ids": subnets,
      "security_group_ids": [aws_lambda_sg(vpc_id,name)]
    },
    environment=lambda_environment_vars)
  
  cw_group = aws.cloudwatch.LogGroup(name,
    name= f"/aws/lambda/lw_{name}",
    retention_in_days=7)
  
  #Generate the role that allows API gateway to execute this lamba
  api_assume_policy = aws.iam.get_policy_document(statements=[{
    "effect": "Allow",
    "principals": [{
        "type": "Service",
        "identifiers": ["apigateway.amazonaws.com"],
    }],
    "actions": ["sts:AssumeRole"],
  }])

  api_lambda_role = aws.iam.Role(f"api_gw_lambda_{name}_role",
    name=f"lw_api_{name}_role",
    assume_role_policy=api_assume_policy.json)
  
  policy_allowApiGwLambdaRun = aws.iam.RolePolicy(f"allowApiGwLambdaRun_{name}",
    name="allowApiGwLambdaRun",
    role=api_lambda_role.id,
    policy= dumps(
      {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "lambda:InvokeFunction",
                "Resource": [
                    f"arn:aws:lambda:{aws.get_region().name}:{aws.get_caller_identity().account_id}:function:lw_{name}"
                ]
            }
        ]
      }))
