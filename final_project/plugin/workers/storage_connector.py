from typing import Iterator, Optional

import psycopg2


class PostgresCredentials:
    def __init__(self):
        self.__user = "db_user"
        self.__dbname = "postgres"
        self.__password = "user123"
        self.__host = "localhost"

    def get_creds(self) -> dict:
        return {
            "user": self.__user,
            "dbname": self.__dbname,
            "password": self.__password,
            "host": self.__host,
        }


class PostgresClient:
    def __init__(self):
        self.psql_cred = PostgresCredentials()

    def __get_creds(self):
        return self.psql_cred.get_creds()

    def get_info_from_db(
            self,
            column: str = "*",
            table: str = "resources",
            where_extension_column: Optional[str] = None,
            where_extension_pattern: Optional[str] = None,
            like: bool = False
    ) -> Iterator:
        """
        The main method to get information from DB.
        :param column: name of column to get from
        :param table: name of table to get from
        :param where_extension_column: name of column to extend with WHERE request
        :param where_extension_pattern: pattern for WHERE request
        :param like: if True, WHERE condition will be changed to: WHERE column LIKE '%pattern%'
        :return: Iterator of got results from DB
        """
        request = f"SELECT {column} FROM {table}"
        if where_extension_column and where_extension_pattern:
            if like:
                request += f" WHERE {where_extension_column} LIKE '%{where_extension_pattern}%' "
            else:
                request += f" WHERE {where_extension_column}='{where_extension_pattern}' "
        with psycopg2.connect(**self.__get_creds()) as connection:
            with connection.cursor() as cursor:
                cursor.execute(request)
                while True:
                    pack_of_data = cursor.fetchmany(10)
                    if pack_of_data:
                        for entry in pack_of_data:
                            yield entry
                    else:
                        break
                connection.commit()


class CICDClient:
    """
    Can be redefined storage to use some API or another type of DB.
    """
    pass
