import os

from dotenv import load_dotenv
from psycopg2 import ProgrammingError, connect

load_dotenv()
user = os.environ["DB_USER"]
host = os.environ["HOST"]
password = os.environ["PASSWORD"]
db = os.environ["DB"]
port = os.environ["PORT"]


def execute_sql(sql_code, *args):
    """
        Executes SQL code with the provided arguments and returns the results.

        Parameters:
            sql_code (str): The SQL code to be executed.
            *args: Variable number of arguments to be passed as parameters to the SQL code.

        Returns:
            list or str: The results of the SQL query as a list of tuples, or an error message as a string if an exception occurs.

        Raises:
            ProgrammingError: If an error occurs during the execution of the SQL code.

    """
    with connect(host=host, user=user, password=password, database=db, port=port) as conn:
        with conn.cursor() as cur:
            cur.execute(sql_code, args)
            try:
                if cur.description is not None:
                    results = cur.fetchall()
                    return results
                else:
                    conn.commit()
            except ProgrammingError:
                raise ProgrammingError
