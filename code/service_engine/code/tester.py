from service import render_service, render_service_field, execute_service
from service_execution import update_service_execution, get_service_execution, search_service_execution
from json import dumps, loads

# event = {
#  'pathParameters':{'pack_name':'blarf','service_name':'feed_cat'},
#  'queryStringParameters':{},
#  'body': {},
#  'headers' : {'Content-Type':'application/json'}
# }
# context ={}

# result = render_service(event=event,context=context)
# print(result)

# #Render a field from a service
# event = {
#  'pathParameters':{'pack_name':'blarf','service_name':'feed_cat', 'field_name':'cat_info'},
#  'queryStringParameters':{},
#  'body': dumps({'cat_name':'Boone'}),
#  'headers' : {'Content-Type':'application/json'}
# }
# context ={}

# result = render_service_field(event=event,context=context)
# print(result)


# event = {
#  'pathParameters':{'pack_name':'blarf','service_name':'feed_cat', 'field_name':'cat_info'},
#  'queryStringParameters':{},
#  'body': dumps({'cat_name':'Boone','cat_info':{'name':"Boone","age":7}}),
#  'headers' : {'Content-Type':'application/json'}
# }
# context ={}

# result = execute_service(event=event,context=context)
# print(result)

# service_execution_id = loads(result['body'])['id']
# body = {
#   "status" : "complete",
#   "result" : {
#     "step" : "a",
#     "status" : "complete",
#     "output" : "Hello there",
#     "error" : ""
#   }
# }
# event = {
#  'pathParameters':{'document_id':service_execution_id},
#  'queryStringParameters':{},
#  'body': dumps(body),
#  'headers' : {'Content-Type':'application/json'}
# }

# result = update_service_execution(event, context)
# print(result)

# event = {
#  'pathParameters':{'document_id':service_execution_id},
#  'queryStringParameters':{},
#  'body': dumps(body),
#  'headers' : {'Content-Type':'application/json'}
# }

# result = update_service_execution(event, context)
# print(result)

body = {
  'status': ["wait for approval"],
  'fields': ['pack', 'service_name', 'status','variables/cat_name']
}
event = {
 'pathParameters':{},
 'queryStringParameters':{},
 'body': dumps(body),
 'headers' : {'Content-Type':'application/json'}
}
context = {}
result = search_service_execution(event, context)
print(result)