from mysql import connector
from mysql.connector import MySQLConnection, InterfaceError
from pydantic import BaseModel, validate_call

from credentials_provider import credentials_provider
from src.db.errors import DataBaseMySQLStillNotExistError


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
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        if fetch_all:
            return cursor.fetchall()
        return cursor.fetchone()

    @validate_call()
    def execute(self, query: str) -> None:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        self.engine.commit()


db = _DataBase(user=credentials_provider.user, password=credentials_provider.password,
               host='db', database='dice_and_die', port='3306')
db.connect()
