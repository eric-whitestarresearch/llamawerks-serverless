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
from pulumi_aws import ec2
from .vpc_endpoint_sg import vpc_endpoint_sg

def vpc_endpoint(name, region, service_name, vpc_id, subnet_ids, sg_ids = [], tags={} ):
  """
  Method to create a vpc endpoint

  Parameters:
    name (String): Name of of the vpc endpoint
    region (String): The region to create the endpoint in
    service_name (String): The name of the serivce for the endpoint
    vpc_id (String): The ID of the VPC to create the endpoint in
    sg_ids (List(String)): The IDs of the Security group to use for the endpoint
    subnet_ids (List(String)): A List of the subnet IDs to associate the endpoints with
    tags (Dict): Optional, a dict of the tags for the endpoint

  Returns
    A pulumi aws ec2 vpc endpoint object
  """

  tags['Name'] = name
  tags['managed_by'] = 'pulumi'

  sg_ids.append(vpc_endpoint_sg(vpc_id, name))

  endpoint = ec2.VpcEndpoint(name,
                             vpc_id=vpc_id,
                             service_name=f"com.amazonaws.{region}.{service_name}",
                             vpc_endpoint_type='Interface',
                             security_group_ids=sg_ids,
                             private_dns_enabled=True,
                             subnet_ids=subnet_ids,
                             tags=tags)
  
  return endpoint