import psycopg2
from psycopg2.extras import execute_values

DATABASE_USERNAME = 'postgres'
DATABASE_PASSWORD = 'admin'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5434'
DATABASE_NAME = 'world'

class DB:
    Instance = None

    @classmethod
    def Connect(cls):
        if cls.Instance is None:
            try:
                cls.Instance = psycopg2.connect(
                    host = DATABASE_HOST,
                    user = DATABASE_USERNAME,
                    password = DATABASE_PASSWORD,
                    port = DATABASE_PORT,
                    dbname = DATABASE_NAME
                )
            except psycopg2.DatabaseError as e:
                print("Error al conectar la base de datos", e)
                raise e
    
    @classmethod
    def SelectRows(cls, query):
        cls.Connect()
        with cls.Instance.cursor() as cursor:
            cursor.execute(query)
            records = [row for row in cursor.fetchall()]
            cursor.close()
        cls.Instance.close()
        cls.Instance = None
        return records




