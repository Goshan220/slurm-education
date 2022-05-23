import yaml
from requests import get

from practice.utils import TypesOfDataDict


class LocalServerManager:
    """
    Class connector to localserver for module 2: Python advanced
    """

    def __init__(self):
        self.__server_ip = "http://127.0.0.1:21122"
        self.__request_path_summary = "/monitoring/infrastructure/using/summary/"
        self.__request_path_prices = "/monitoring/infrastructure/using/prices"
        self.__parsed_input_data = {}

    @property
    def parsed_input_data(self):
        return self.__parsed_input_data

    @parsed_input_data.setter
    def parsed_input_data(self, value):
        self.__parsed_input_data = value

    def get_summary_from_server(self, seed: int = 1):
        """
        Do request with 'requests' lib to local server.
        :return: raw data from server
        """
        response = get(url=f"{self.__server_ip}{self.__request_path_summary}{seed}").text
        return response

    def get_prices_from_server(self):
        resource = get(url=f"{self.__server_ip}{self.__request_path_prices}").text
        return resource

    def parse_raw_input_to_dict(self, input_data: str = "") -> dict:
        """
        Function parses the input data into a convenient option for processing
        :param input_data: data from get_input_from_server function
        :returns: dict with parsed data: {"team_name": [{"resource_id: "some_id", "measurement": "CPU", "data"...} ,
        {{"resource_id: "some_id", "measurement": "GPU", ...}, ...]}
        """
        if not input_data:
            input_data = self.get_summary_from_server()
        split_by_teams = input_data.split("$")
        summary_data = yaml.safe_load(self.get_prices_from_server())
        for team in split_by_teams:
            team_name, team_data = team.split("|")
            team_data_list = []
            for data in team_data.split(";"):
                split_data = data.strip("()").split(",")
                price = summary_data.get("values").get(split_data[0]).get(split_data[1])
                team_data_list.append(
                    {
                        TypesOfDataDict.resource_id: split_data[0],
                        TypesOfDataDict.measurement: split_data[1],
                        TypesOfDataDict.date_time: split_data[2],
                        TypesOfDataDict.load: split_data[3],
                        TypesOfDataDict.price: price,
                    }
                )
            self.__parsed_input_data[team_name] = team_data_list
        return self.parsed_input_data
