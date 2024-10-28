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
from pulumi_aws import ec2, vpc

def vpc_endpoint_sg(vpc_id, endpoint_name):
  """
  Create a Security group that allows the VPC to access a VPC Endpoint

  Parameters:
    vpc_id (String): The ID of the VPC the endpoint is created in
    endpoint_name: THe name of the VPC endpoint

  Returns:
    A pulumi object with a vpc endpoint
  """

  target_vpc = ec2.get_vpc(id=vpc_id)
  sg_name = f"{endpoint_name}_vpc_ep_sg"
  tags = {
    "Name": sg_name,
    "managed_by": "pulumi"
  }
  vpc_ep_sg = ec2.SecurityGroup(sg_name,
                                name = sg_name,
                                description="Allow VPC to access endpoint",
                                vpc_id=vpc_id,
                                tags=tags)
  
  vpc_ep_sg_ingress_rule = vpc.SecurityGroupIngressRule("allow_vpc_ep",
                                                        security_group_id=vpc_ep_sg.id,
                                                        cidr_ipv4=target_vpc.cidr_block,
                                                        from_port=443,
                                                        to_port=443,
                                                        ip_protocol='tcp')
  
  return vpc_ep_sg
  