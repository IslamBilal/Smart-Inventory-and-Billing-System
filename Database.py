#Database Connection Settings
import psycopg2


def connection():
    con = psycopg2.connect(
        host="localhost",
        database="ecommerce",
        user="postgres",
        password="1234",
        port="5432"
    )

    if con:
        print("Connention successful")
    else:
        print("Connection failed")
    return con
conn = connection()