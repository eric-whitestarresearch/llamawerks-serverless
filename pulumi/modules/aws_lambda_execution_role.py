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

def aws_lambda_execution_role():
  """
  Creates the execution role for the llamawerks lamba functions

  Parameters:
    None

  Returns:
    Pulumi role object
  """

  assume_policy = aws.iam.get_policy_document(statements=[{
    "effect": "Allow",
    "principals": [{
        "type": "Service",
        "identifiers": ["lambda.amazonaws.com"],
    }],
    "actions": ["sts:AssumeRole"],
  }])

  lambda_role = aws.iam.Role(f"llamaweks_lambda_execution_role",
    name="llamaweks_lambda_execution_role",
    assume_role_policy=assume_policy.json)


  policy_allowKmsDecrypt = aws.iam.RolePolicy("lw_allowKmsDecrypt",
    name="allowKmsDecrypt",
    role=lambda_role.id,
    policy = dumps(
      {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": "kms:Decrypt",
                "Resource": f"arn:aws:kms:*:{aws.get_caller_identity().account_id}:key/*"
            }
        ]
      }))
  
  policy_allowSSMParameterDBConfig = aws.iam.RolePolicy("lw_allowSSMParameterDBConfig",
    name="allowSSMParameterDBConfig",
    role=lambda_role.id,
    policy =dumps(
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "ssm:GetParameter",
            "Resource": f"arn:aws:ssm:{aws.get_region().name}:{aws.get_caller_identity().account_id}:parameter/llamawerks_db_config"
          }
          ] 
      }))

  policy_lambdaExecution = aws.iam.RolePolicy("lw_lambdaExecution",
    name="lambdaExecution",
    role=lambda_role.id,
    policy= dumps(
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": f"arn:aws:logs:{aws.get_region().name}:{aws.get_caller_identity().account_id}:*"
          },
          {
            "Effect": "Allow",
            "Action": [
              "logs:CreateLogStream",
              "logs:PutLogEvents"
            ],
            "Resource": [
              f"arn:aws:logs:{aws.get_region().name}:{aws.get_caller_identity().account_id}:log-group:/aws/lambda/lw_*:*"
            ]
          }
        ]
     }))
        
  policy_allowVpcNicAdd = aws.iam.RolePolicy("lw_allowVpcNicAdd",
    name="allowVpcNicAdd",
    role=lambda_role.id,
    policy= dumps(
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
              "ec2:CreateNetworkInterface",
              "ec2:DescribeInstances",
              "ec2:DescribeNetworkInterfaces",
              "ec2:CreateTags",
              "ec2:DeleteNetworkInterface",
              "ec2:AttachNetworkInterface"
            ],
            "Resource": "*"
          }
        ]
      }))
  
  return lambda_role