# +
from sqlalchemy import create_engine
import psycopg2

def dbconfig():
    
    db = {"host": "affordablehousing.a2hosted.com",
            "port": 5432,
            "database": "afford31_housing",
            "user": "afford31_siads",
            "pass": "NpSs7M!vAHhQrD1Z8e@!N7*kQZZ4"}
    pg_string = f"postgresql://{db['user']}:{db['pass']}@{db['host']}:{db['port']}/{db['database']}"
    database_engine = create_engine(pg_string, echo = False)
    return database_engine
# -


