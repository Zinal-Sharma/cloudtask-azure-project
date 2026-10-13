#database connection

import os
from mssql_python import connect
from keyvault import get_secret


def get_connection():
    server = os.environ["DB_SERVER"]
    database = os.environ["DB_NAME"]
    username = os.environ["DB_USER"]

    password = get_secret("CloudTaskDatabasePassword")

    connection_string = (
        f"Server={server};"
        f"Database={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
    )

    return connect(connection_string)