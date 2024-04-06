from flask import Flask
from flask_restful import Api, Resource, abort
from flask_cors import CORS
from config import Config
from db import get_db_connection
from flask_caching import Cache

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True)
app.config.from_object(Config)
cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': app.config['REDIS_HOST'],
    'CACHE_REDIS_PORT': app.config['REDIS_PORT'],
})
cache.init_app(app)
api = Api(app)

class HelloWorld(Resource):
    @cache.cached(timeout=300)
    def get(self):
        return {'greeting': 'Hello, World!'}
    
class CreateRecordTable(Resource):
    def get(self):
        try:
            connection = get_db_connection()
            if connection is None:
                raise Exception("Could not connect to database")
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE record (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                )
                """
            )
            connection.commit()
            connection.close()
            return {'message': 'Table created successfully'}
        except Exception as ex:
            return abort(500, message=f"Failed to create table. Error: {ex}")

class CreateRecord(Resource):
    def get(self):
        try:
            connection = get_db_connection()
            if connection is None:
                raise Exception("Could not connect to database")
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO record (name) VALUES ('John Doe')
                """
            )
            connection.commit()
            connection.close()
            return {'message': 'Record created successfully'}
        except Exception as ex:
            return abort(500, message=f"Failed to create record. Error: {ex}")

class GetRecord(Resource):
    @cache.cached(timeout=30)
    def get(self):
        try:
            connection = get_db_connection()
            if connection is None:
                raise Exception("Could not connect to database")
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT * FROM record
                """
            )
            items = cursor.fetchall()
            connection.close()
            return {'records': items}
        except Exception as ex:
            return abort(500, message=f"Failed to get records. Error: {ex}")

api.add_resource(CreateRecordTable, '/create-record-table')
api.add_resource(CreateRecord, '/create-record')
api.add_resource(GetRecord, '/get-record')
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
