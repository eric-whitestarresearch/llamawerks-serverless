from service import render_service, render_service_field
from json import dumps

event = {
 'pathParameters':{'pack_name':'blarf','service_name':'feed_cat'},
 'queryStringParameters':{},
 'body': {},
 'headers' : {'Content-Type':'application/json'}
}
context ={}

result = render_service(event=event,context=context)
print(result)

#Render a field from a service
event = {
 'pathParameters':{'pack_name':'blarf','service_name':'feed_cat', 'field_name':'cat_info'},
 'queryStringParameters':{},
 'body': dumps({'cat_name':'Boone'}),
 'headers' : {'Content-Type':'application/json'}
}
context ={}

result = render_service_field(event=event,context=context)
print(result)