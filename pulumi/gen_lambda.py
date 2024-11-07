import yaml

lambda_fuctions = []
with open('./pulumi/functions_list.txt','r') as file:
      for line in file:
        fname = line.rstrip()
        lambda_fuction = {
            'name': fname.replace('.','_'),
            'handler': fname,
            'package_location': "../code/service_engine/package.zip",
            'package_checksum_location' :  "../code/service_engine/package.sum"
        }
        lambda_fuctions.append(lambda_fuction)

with open('lambda.yaml','w') as outfile:
      yaml.dump(lambda_fuctions, outfile, default_flow_style=False)

