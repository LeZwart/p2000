import pyodbc
import json


def connect(database):
    """Connect to the SQL Server database and return the connection object
    Args:
        database (str): The name of the database to connect to.
    Returns:
        conn (pyodbc.Connection): The connection object to the database.
    Raises:
        pyodbc.Error: If there is an error connecting to the database.
    """

    with open("database.json") as file:
        config = json.load(file)

        DRIVER = "ODBC Driver 18 for SQL Server"
        SERVER = config["server"]
        DATABASE = database
        USERNAME = config["username"]
        PASSWORD = config["password"]

        try:
            conn = pyodbc.connect(
                f"DRIVER={DRIVER};"
                f"SERVER={SERVER};"
                f"DATABASE={DATABASE};"
                f"UID={USERNAME};"
                f"PWD={PASSWORD};"
                f"Encrypt=yes;"
                f"TrustServerCertificate=yes;"
            )
            return conn

        except pyodbc.Error as e:
            print(f"Error connecting to database: {e}")
            return None


def table_exists(cursor, table_name):
    """Check if a table exists in the database"""
    cursor.execute(
        """
        SELECT CASE
            WHEN EXISTS (
                SELECT 1
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME = ?
            ) THEN 1
            ELSE 0
        END AS TableExists;
        """,
        (table_name,)
    )
    return cursor.fetchone()[0] == 1


def record_with_key(cursor, table_name, key, value):
    """Check if a record with a specific key exists in the table"""
    cursor.execute(
        f"SELECT 1 FROM [{table_name}] WHERE [{key}] = ?",
        (value,)
    )
    return cursor.fetchone() is not None


def create_table(
    cursor, table_name, columns, primary_key=None, foreign_keys=None
):
    """Create a table in the database with optional primary and foreign keys"""
    column_definitions = []

    for column in columns:
        column_definitions.append(f"[{column}] NVARCHAR(4000)")

    if primary_key:
        if isinstance(primary_key, str):
            primary_key = [primary_key]
        column_definitions.append(
            f"PRIMARY KEY ({', '.join([f'[{pk}]' for pk in primary_key])})"
        )

    if foreign_keys:
        for fk in foreign_keys:
            column_definitions.append(
                f"FOREIGN KEY ([{fk['column']}]) "
                f"REFERENCES [{fk['ref_table']}]([{fk['ref_column']}])"
            )

    stmt = f"CREATE TABLE [{table_name}] ({', '.join(column_definitions)});"
    cursor.execute(stmt)
    print(f"Table '{table_name}' created successfully.")


def insert_into_table(cursor, table_name, data):
    """Insert data into a table"""
    column_length = len(data.keys())
    insert_stmt = (
        f"INSERT INTO [{table_name}] ("
        f"{', '.join([f'[{key}]' for key in data.keys()])}) "
        f"VALUES ("
        f"{', '.join(['?' for _ in range(column_length)])})"
    )
    cursor.execute(insert_stmt, list(data.values()))
