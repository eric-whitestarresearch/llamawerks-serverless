from modules.database import Database
import modules.logger

db = Database()

result = db.find_in_collection('newtable','$.age ==7 && $.hair_length == "short"')
print(f"find one: {result}")

result = db.find_in_collection('newtable','$.age ==9 && $.hair_length == "short"')
print(f"find none: {result}")
      
      
result = db.find_in_collection('newtable','', find_many=True, projection=('name','age'))
print(f"find many: {result}")

result = db.find_in_collection('newtable','$.age ==9', find_many=True, projection=('name','age'))
print(f"find none on many: {result}")