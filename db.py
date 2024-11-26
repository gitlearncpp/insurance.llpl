import psycopg2
from psycopg2.extras import RealDictCursor

# Data to connecting with DB - for test only, PRD - another data
def create_connection():
    return psycopg2.connect(
        dbname="insurance_db",
        user="cisco",
        password="Niestety123",
        host="localhost",
        port="5432"
    )
