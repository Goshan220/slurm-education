import requests


class TypesOfLoad:
    decrease = "decrease"
    surges = "surges"
    stable = "stable"


class TypesOfIntesity:
    low = "low"
    middle = "middle"
    high = "high"
    enormous = "enormous"


class ServerConnector:
    def __init__(self):
        self.__server_host = "http://127.0.0.1:21122"
        self.__request_path = "/monitoring/infrastructure/using/summary/1"

    def get_input_from_server(self):
        response = requests.get(url=f"{self.__server_host}{self.__request_path}").text
        return response


class STODATAParser:
    def __init__(self):
        self.__parsed_input_data = {}
        self.__analyzed_data = {}

    @property
    def parsed_input_data(self):
        return self.__parsed_input_data

    @parsed_input_data.setter
    def parsed_input_data(self, value):
        self.__parsed_input_data = value

    def parse_input_to_dict(self, input_data: str):
        """
        function parses the input data into a convenient option for processing
        :param input_data: data to parse
        """
        split_by_teams = input_data.split("$")
        for team in split_by_teams:
            split_ = team.split("|")
            team_name_ = split_[0]
            team_data = split_[1].split(";")
            team_data_list = []
            for data in team_data:
                split_data = data.strip("()").split(",")
                team_data_list.append({
                    "resource_id": split_data[0],
                    "measurement": split_data[1],
                    "data_time": split_data[2],
                    "load": split_data[3]
                })
            self.parsed_input_data[team_name_] = team_data_list

    @staticmethod
    def __fill_base_info(team_data: list, required_dict: dict) -> dict:
        for data in team_data:
            resource_id = data.get("resource_id")
            measurement = data.get("measurement")
            load = data.get("load")

            required_dict.setdefault(resource_id, {}).setdefault(measurement, {}).setdefault("load", [])
            required_dict[resource_id][measurement]["load"].append(int(load))
        return required_dict

    @staticmethod
    def calculate_average(list_of_values: list[int]):
        return sum(list_of_values) / len(list_of_values)

    @staticmethod
    def calculate_median(list_of_values: list[int]):
        quotient, remainder = divmod(len(list_of_values), 2)
        return list_of_values[quotient] if remainder else sum(list_of_values[quotient - 1:quotient + 1]) / 2

    def __fill_average(self, analytics_dict) -> dict:
        for resource_id, measurements in analytics_dict.items():
            for measurement, values in measurements.items():
                # list_of_loads = sorted(values.get("load"))
                list_of_loads = analytics_dict[resource_id][measurement].pop("load")

                average = self.calculate_average(list_of_loads)
                median = self.calculate_median(list_of_loads)
                analytics_dict[resource_id][measurement].update({
                    'Среднее измерения': average, 'Медиана измерения': median
                })
        return analytics_dict

    @staticmethod
    def calculate_load_type(average, median) -> str:
        status = None
        try:
            ratio = int(average / median * 100)
            if ratio < 75:
                status = TypesOfLoad.decrease
            elif ratio > 125:
                status = TypesOfLoad.surges
            else:
                status = TypesOfLoad.stable
        except ZeroDivisionError:
            print("median is 0, return status stable")
            status = TypesOfLoad.stable
        finally:
            return status

    @staticmethod
    def calculate_intensity(median: int) -> str:
        # if 0 < median <= 30:
        # или я где то обсчитался, или в медиана может всё таки быть равной нулю,
        # т.к. на некоторых данных выпадает ValueError
        if 0 <= median <= 30:
            status = TypesOfIntesity.low
        elif 30 < median <= 60:
            status = TypesOfIntesity.middle
        elif 60 < median <= 90:
            status = TypesOfIntesity.high
        elif median > 90:
            status = TypesOfIntesity.enormous
        else:
            raise ValueError(f"incorrect value: {median}, can't be lower that 0")
        return status

    @staticmethod
    def calculate_decision(load_type, intensity):
        if (intensity == TypesOfIntesity.low) or \
                (intensity == TypesOfIntesity.middle and load_type == TypesOfLoad.decrease):
            decision = "delete resource"
        elif (intensity == TypesOfIntesity.middle) and \
                (load_type == TypesOfLoad.stable or load_type == TypesOfLoad.surges):
            decision = "normal using"
        elif (intensity == TypesOfIntesity.high) and \
                (load_type == TypesOfLoad.decrease or load_type == TypesOfLoad.stable):
            decision = "normal using"
        elif (load_type == TypesOfLoad.surges) and (intensity == TypesOfIntesity.high) or \
                intensity == TypesOfIntesity.enormous:
            decision = "extend resource"
        else:
            raise Exception(f"raw decision: {load_type} {intensity}")
        return decision

    def __fill_analytic_info(self, analytics_dict):
        for resource_id, measurements in analytics_dict.items():
            for measurement, values in measurements.items():
                average = analytics_dict[resource_id][measurement]['Среднее измерения']
                median = analytics_dict[resource_id][measurement]['Медиана измерения']

                load_type = self.calculate_load_type(average, median)
                analytics_dict[resource_id][measurement]['Тип использования'] = load_type

                intensity = self.calculate_intensity(median)
                analytics_dict[resource_id][measurement]['Интенсивность использования'] = intensity

                decision = self.calculate_decision(load_type, intensity)
                analytics_dict[resource_id][measurement]['решение'] = decision
        return analytics_dict

    def calculate_data_analytic_for_team(self, team_name_) -> dict:
        """
        main function calculating all required data for provided team name
        :param team_name_: name of team to calculate
        :return: dict with all calculated data for team
        """
        team_data = self.parsed_input_data[team_name_]
        analytics_dict = {}
        analytics_dict = self.__fill_base_info(team_data, analytics_dict)
        analytics_dict = self.__fill_average(analytics_dict)
        analytics_dict = self.__fill_analytic_info(analytics_dict)
        self.__analyzed_data.update({team_name_: analytics_dict})
        # print(analytics_dict)
        return analytics_dict

    def create_report(self, team_name_):
        team_data = self.__analyzed_data.get(team_name_, None)
        if not team_data:
            team_data = self.calculate_data_analytic_for_team(team_name_)
        print("|Resource|Dimension|mean|mediana|usage_type|intensivity|decision|")
        for resource_id, measurements in team_data.items():
            for measurement, values in measurements.items():
                list_to_show = [
                    resource_id,
                    measurement,
                    str(team_data[resource_id][measurement]['Среднее измерения']),
                    str(team_data[resource_id][measurement]['Медиана измерения']),
                    str(team_data[resource_id][measurement]['Тип использования']),
                    str(team_data[resource_id][measurement]['Интенсивность использования']),
                    str(team_data[resource_id][measurement]['решение']),
                ]
                print(f"|{'|'.join(list_to_show)}|")


if __name__ == '__main__':
    connector = ServerConnector()
    sto_data_parser = STODATAParser()
    sto_data_parser.parse_input_to_dict(input_data=connector.get_input_from_server())
    for team_name in sto_data_parser.parsed_input_data.keys():
        # sto_data_parser.calculate_data_analytic_for_team(team_name)
        print("\n" * 2 + team_name)
        sto_data_parser.create_report(team_name)
