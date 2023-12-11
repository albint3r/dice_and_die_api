from mysql import connector
from mysql.connector import MySQLConnection, InterfaceError
from pydantic import BaseModel

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


db = _DataBase(user='root', password='root',
               host='db', database='dice_and_die',
               port='3306')
db.connect()
