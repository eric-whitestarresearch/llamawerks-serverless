from data_collection import create_data_collection

body = """
 {
    "name": "narf",
    "pack": "narf",
    "fields": [
      {
        "name": "$ne.name",
        "type": "string",
        "required": true,
        "index": true,
        "unique": true
      }
    ]
  }

"""
event = {
 'pathParameters':{'pack_name':'narf'},
 'queryStringParameters':{},
 'body': body,
 'headers' : {'Content-Type':'application/json'}
}
context ={}

result = create_data_collection(event=event,context=context)
print(result)