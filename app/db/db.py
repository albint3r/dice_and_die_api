import time

import mysql.connector as connector
from mysql.connector import Error as DBError, MySQLConnection
from pydantic import BaseModel

from credentials_provider import credentials_provider


class _DataBase(BaseModel):
    user: str
    password: str
    host: str
    database: str
    port: str
    connection: MySQLConnection | None = None

    class Config:
        arbitrary_types_allowed = True

    def _execute_query(self, query: str, values: list | tuple, fetch_all: bool = False) -> list[dict] | dict:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, values)
        result = cursor.fetchall() if fetch_all else cursor.fetchone()
        cursor.close()
        return result

    def connect(self, attempts: int = 3, delay: int = 2) -> None:
        attempt = 1
        while attempt <= attempts:
            try:
                self.connection = connector.connect(user=self.user, password=self.password,
                                                    host=self.host, database=self.database,
                                                    port=self.port, auth_plugin='mysql_native_password')
                return
            except (DBError, IOError) as _:
                if attempt == attempts:
                    # Log the error here
                    return
                time.sleep(delay ** attempt)
                attempt += 1

    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()

    def query(self, query: str, values: list | tuple, fetch_all: bool = False) -> list[dict] | dict:
        try:
            self.connect()
            result = self._execute_query(query, values, fetch_all)
            self.disconnect()
            return result
        except DBError as e:
            # Log the error here
            raise e

    def execute(self, query: str, values: list | tuple) -> None:
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            self.disconnect()
        except DBError as e:
            # Log the error here
            raise e


db = _DataBase(user=credentials_provider.user,
               password=credentials_provider.password,
               host='db', database='dice_and_die', port='3306')
