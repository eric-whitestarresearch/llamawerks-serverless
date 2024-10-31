import json

def echo(event, context):
  return {
    "statusCode":200, "body": json.dumps(event), "headers": {}
  }
