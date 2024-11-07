import data_collection

event = {"pathParameters":{"pack_name": "blarf"},"queryStringParameters":{ "data_collection_name": "blarf"}}
context = None

print(data_collection.get_data_collections(event, context))