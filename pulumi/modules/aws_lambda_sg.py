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

from pulumi_aws import ec2, vpc

def aws_lambda_sg(vpc_id, lambda_name):
  """
  Create a Security group used by the VPC Connection of a Lambda function

  Parameters:
    vpc_id (String): The ID of the VPC the lambda is created in
    lambda_name: The name of the lambda function

  Returns:
    A pulumi object with a security group
  """

  target_vpc = ec2.get_vpc(id=vpc_id)
  sg_name = f"{lambda_name}_lambda_sg"
  tags = {
    "Name": sg_name,
    "managed_by": "pulumi"
  }
  aws_lambda_sg = ec2.SecurityGroup(sg_name,
                                name = sg_name,
                                description="Allow Lambda VPC Access",
                                vpc_id=vpc_id,
                                tags=tags)
  
  aws_lambda_sg_ingress_rule = vpc.SecurityGroupIngressRule(f"allow_lambda_vpc_{lambda_name}",
                                                        security_group_id=aws_lambda_sg.id,
                                                        cidr_ipv4=target_vpc.cidr_block,
                                                        ip_protocol=-1)
  
  aws_lambda_sg_egress_rule = vpc.SecurityGroupEgressRule(f"allow_lambda_out_{lambda_name}",
                                                          security_group_id=aws_lambda_sg.id,
                                                          cidr_ipv4="0.0.0.0/0",
                                                          ip_protocol=-1)
  
  
  return aws_lambda_sg
  