import psycopg2

from utils import TypesOfDataDict


class BaseCredentials:
    def get_creds(self):
        raise NotImplementedError("this method should be defined in subclass")


class PostgresCredentials(BaseCredentials):
    def __init__(self):
        self.__user = "postgres"
        self.__dbname = "postgres"
        self.__password = "q1w2e3"
        self.__host = "localhost"

    def get_creds(self) -> dict:
        return {
            "user": self.__user,
            "dbname": self.__dbname,
            "password": self.__password,
            "host": self.__host,
        }


class DBManager:
    """
    Class connector to database from module 3
    """

    def __init__(self):
        self.__parsed_input_data = {}

    @property
    def parsed_input_data(self):
        return self.__parsed_input_data

    @parsed_input_data.setter
    def parsed_input_data(self, value):
        self.__parsed_input_data = value

    @staticmethod
    def __get_creds(creds: BaseCredentials):
        return creds.get_creds()

    def get_data_from_db(self):
        """
        Get data from database on localhost
        :return: list with objects
        """
        with psycopg2.connect(**self.__get_creds(PostgresCredentials())) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usage_stats.resources")
                while True:
                    pack_of_data = cursor.fetchmany(10)
                    if pack_of_data:
                        for entry in pack_of_data:
                            yield entry
                    else:
                        break
                connection.commit()

    def parse_data_from_db(self, input_data: list = None):
        """
        Function parses the data from db into a convenient option for processing
        :param input_data: data from get_data_from_db function
        :returns: dict with parsed data: {"team_name": [{"resource_id: "some_id", "measurement": "CPU", "data"...} ,
        {{"resource_id: "some_id", "measurement": "GPU", ...}, ...]}
        """
        if input_data is None:
            input_data = self.get_data_from_db()
        for entry in input_data:
            team_name = entry[2]
            team_data = {
                TypesOfDataDict.resource_id: entry[1],
                TypesOfDataDict.measurement: entry[3],
                TypesOfDataDict.date_time: entry[4],
                TypesOfDataDict.load: int(entry[5]),
            }
            self.__parsed_input_data.setdefault(team_name, []).append(team_data)
        return self.parsed_input_data
