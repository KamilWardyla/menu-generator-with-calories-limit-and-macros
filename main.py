import os
from psycopg2 import connect, ProgrammingError
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()
user = os.environ["DB_USER"]
host = os.environ["HOST"]
password = os.environ["PASSWORD"]
db = os.environ["DB"]


def execute_sql(sql_code, *args):
    with connect(host=host, user=user, password=password, database=db) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql_code, args)
            try:
                results = cur.fetchall()
            except ProgrammingError as e:
                return f"Error {e}"
