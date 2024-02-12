from abc import ABC

from icecream import ic
from mysql import connector
from mysql.connector import MySQLConnection, InterfaceError
from pydantic import BaseModel, validate_call

from credentials_provider import credentials_provider
from src.db.errors import DataBaseMySQLStillNotExistError
import mysql.connector


class _DataBase(BaseModel):
    user: str
    password: str
    host: str
    database: str
    port: str
    connection: MySQLConnection | None = None

    class Config:
        arbitrary_types_allowed = True

    def connect(self) -> None:
        try:
            self.connection = connector.connect(user=self.user, password=self.password,
                                                host=self.host, database=self.database,
                                                port=self.port, auth_plugin='mysql_native_password')
        except InterfaceError:
            raise DataBaseMySQLStillNotExistError("Data Base don't exist yet. Restart the program.")

    @validate_call()
    def query(self, query: str, fetch_all: bool = False) -> list[dict] | dict:
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            return cursor.fetchall() if fetch_all else cursor.fetchone()
        except mysql.connector.Error as err:
            ic('I left this comment to have a break point if a watch the logs again and this dont work to fix the bug')
            if err.errno == mysql.connector.errorcode.CR_SERVER_GONE_ERROR:
                # Reconectar
                self.connection.reconnect()
                cursor = self.connection.cursor()
                cursor.execute(query)
                return cursor.fetchall() if fetch_all else cursor.fetchone()
            else:
                # Manejar otros errores
                ic("Error:", err)

    @validate_call()
    def execute(self, query: str) -> None:
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as err:
            ic('I left this comment to have a break point if a watch the logs again and this dont work to fix the bug')
            if err.errno == mysql.connector.errorcode.CR_SERVER_GONE_ERROR:
                self.connection.reconnect()
                cursor = self.connection.cursor(dictionary=True)
                cursor.execute(query)
                self.connection.commit()
            else:
                # Manejar otros errores
                ic("Error:", err)


class AbstractDB(BaseModel, ABC):
    db: _DataBase

    @validate_call()
    def query(self, query: str, fetch_all: bool = False) -> list[dict] | dict:
        """Create a SQL Query to fetch data. By default, you fetch only one element of the query."""
        return self.db.query(query=query, fetch_all=fetch_all)

    @validate_call()
    def execute(self, query: str) -> None:
        """This executes the query and commit the result"""
        self.db.execute(query=query)


db = _DataBase(user=credentials_provider.user, password=credentials_provider.password,
               host='db', database='dice_and_die', port='3306')
db.connect()
