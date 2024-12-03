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


from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId, json_util
from jsonschema import validate, ValidationError
from urllib.parse import quote_plus
import os
from bson.json_util import dumps
from json import loads
import logging

class DBConfigValidationError(ValidationError):
  pass

class DBConnectionFailure(ConnectionFailure):
  pass

class MissingDBHost(BaseException):
  pass

class MissingDBDatabase(BaseException):
  pass
class MissingAWSToken(BaseException):
  pass

class Database:
  """
  This is a class used for accessing the database. When initialize it it open a connection to the database. 
  The config for the database connection comes from /opt/self-service-portal/conf/db.conf

  Attributes:
      mongo_client (MongoClient): The client class for the db connection
      datbase (Database): The database the client is connected to
      collection (Collection): The collection that the client is connect to
  """
  
  database_name = ""
  connection = None

  def __init__(self) -> None:
    """
    The constructor for the Database class.

    Parameters:
      self (Database): The object itself
    """

    logging.info("Databse INIT")

    aws_session_token = os.environ.get('AWS_SESSION_TOKEN')
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    mongodb_host = os.environ.get('MONGODB_HOST')
    mongodb_database = os.environ.get('MONGODB_DATABASE')
    
    try:
      assert aws_access_key_id and aws_secret_access_key and aws_session_token
    except AssertionError:
      raise MissingAWSToken("The environment variables for aws access tokens are not set. Require: AWS_SESSION_TOKEN, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
    
    try:
      assert mongodb_host
    except AssertionError:
      raise MissingDBHost("Missing the MONGODB_HOST environment variable")
    
    try:
      assert mongodb_database
    except AssertionError:
      raise MissingDBDatabase("Missing the MONGODB_DATABASE environment variable")
  
    logging.info(f"Connecting to db host: {mongodb_host} database: {mongodb_database} ")
    
    connection_string = f"mongodb+srv://{mongodb_host}/?authSource=%24external&authMechanism=MONGODB-AWS"
    
    self.connection =  MongoClient(connection_string,tls=True)
    self.database_name = mongodb_database


  def __del__(self):
    """
    Close all connections to the database in prep for shutdown

    Parameters:
      self (Database): The object itself.

    Returns:
      None
    """

    self.connection.close()

    return
  
  def validate_config(self, config) -> None:
    """
    This is a method that validates the contents of the DB config file

    Parameters:
      self (Database): The object itself.
      config (Dict): A dictonary containing the config
    
    Returns:
      None
    """

    schema = {
      '$schema': 'http://json-schema.org/draft-04/schema#',
      'type': 'object',
      'properties': {
        'protocol': {'type':'string'},
        'host': {'type': 'string'},
        'port': {'type': 'integer'},
        'tls': {'type': 'boolean'},
        'database': {'type': 'string'},
        'username': {'type': 'string'},
        'password': {'type': 'string'}
      },
      'required': ['protocol', 'host', 'port', 'database', 'username', 'password']}

    validate(config, schema) #If we validate nothing happens, if we fail a ValidationError exception is thrown

    return None
  
  def get_db_connection(self) -> MongoClient:
    """
    Get a connection from the database pool

    Parameters:
      self (Database): The object itself.

    Returns:
      (MongoClient): A connection to the database
    """
    
    return self.connection
  
  def return_db_connection(self, connection):
    """
    Returns a DB connection to the pool

    Parameters:
      self (Database): The object itself.
      connection (MongoClient): A connection to the database

    Returns
      None
    """
    # The serverless version of the code doesn't use connection pooling. So this does nothing. 
    # I'll probably refactor it out later. 
    pass
  
  def find_all_in_collection(self, collection, filter, projection = {}):
    """
    Find all documents in a collection

    Parameters:
      self (Database): The object itself.
      collection (String): The name of the collection to search in
      filter (Dict): A dictonary containing the filter to search by 

    Returns:
      List: A list of all of the documents found
    """

    connection = self.get_db_connection()
    db = connection[self.database_name]
    db_collection = db[collection]
    

    pipeline = [{'$match' : filter}, {'$addFields': {"id": {'$toString': "$_id"}}},{'$project': { "_id":0 } | projection }]

    try:
      results = db_collection.aggregate(pipeline)
    finally:
      self.return_db_connection(connection)

    documents = (loads(dumps(results)))

    return documents
  
  def insert_document(self, collection, document):
    """
    A function to insert a new doument

    Parameters:
      self (Database): The instantiation of the Database class
      document (Dict): A dictonary with the document to inset into a collection

    Returns:
      Str: A 24 character hexadecmal string that represents the id of the new object
    """

    connection = self.get_db_connection()
    db = connection[self.database_name]
    db_collection = db[collection]

    try:
      result = db_collection.insert_one(document)
    finally:
      self.return_db_connection(connection)
    
    return str(result.inserted_id)

  def update_document(self, collection, filter, values_to_update, upsert=False):
    """
    Finds a document in a collection

    Parameters:
      self (Database): The object itself.
      collection (String): The name of the collection to search in
      filter (Dict): A dictonary containing the filter to search by 
      values_to_updates (Dict): The values to update in the document
      upsert (Bool): Insert a new document if it does not exist, defaults to false

    Returns:
      Int: The count of updated documents
    """

    connection = self.get_db_connection()
    db = connection[self.database_name]
    db_collection = db[collection]

    try:
      result = db_collection.update_many(filter, { "$set": values_to_update}, upsert)  
    finally:
      self.return_db_connection(connection)

    return result.modified_count

  def delete_document(self, collection, filter):
    """
    Deletes document(s) in a collection

    Parameters:
      self (Database): The object itself.
      collection (String): The name of the collection to search in
      filter (Dict): A dictonary containing the filter to search by 
    
    Returns:
      Int: The count of deleted documents
    """
    connection = self.get_db_connection()
    db = connection[self.database_name]
    db_collection = db[collection]

    try:
      result = db_collection.delete_many(filter)  
    finally:
      self.return_db_connection(connection)

    return result.deleted_count
  
  def create_index(self, collection, keys, unique):
    """
    Creates a collection in the database

    Parameters:
      self (Database): The object itself.
      collection (String): The name of the collection to create
      keys (List or Str): Either a list of keys names to create the index for onn compound index, or just a string for a single key


    Returns:
      Str
    """

    connection = self.get_db_connection()
    db = connection[self.database_name]
    db_collection = db[collection]

    try:
      result = db_collection.create_index(keys, background=True, unique=unique)
    finally:
      self.return_db_connection(connection)

    return result
  
  def get_index_info(self, collection):
    """
    Returns the existing indexes in the collection

    Parameters:
      self (Database): The object itself.
      collection (String): The name of the collection to fetch the index for

    Returns:
      Dict: A dictonary of the index. The dictonary key is the index name, the value is the index info
    """

    connection = self.get_db_connection()
    db = connection[self.database_name]
    db_collection = db[collection]

    try:
      result = db_collection.index_information()
    finally:
      self.return_db_connection(connection)

    return result
  
  def delete_index(self, collection, index_name):
    """
    Drops an index from a collection
    
    Parameter:
      self (Database): The object itself.
      collection (String): The name of the collection is in
      index_name (String): The name of the index to drop

    Returns:
      None
    """

    connection = self.get_db_connection()
    db = connection[self.database_name]
    db_collection = db[collection]

    try:
      db_collection.drop_index(index_name)
    finally:
      self.return_db_connection(connection)

    return
  
  def delete_collection(self, collection):
    """
    Drops a collection
    
    Parameter:
      self (Database): The object itself.
      collection (String): The name of the collection to drop

    Returns:
      None
    """
   
    connection = self.get_db_connection()
    db = connection[self.database_name]
    db_collection = db[collection]

    try:
      db_collection.drop()
    finally:
      self.return_db_connection(connection)

    return