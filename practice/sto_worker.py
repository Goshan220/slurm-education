import datetime

from practice.utils import TypesOfDataDict, TypesOfLoad, TypesOfIntensity


class STOWorker:
    def __init__(self, input_data=None):
        if input_data is None:
            input_data = {}
        self.__parsed_input_data = input_data
        self.__analyzed_data = {}

    @property
    def parsed_input_data(self):
        return self.__parsed_input_data

    @parsed_input_data.setter
    def parsed_input_data(self, value):
        self.__parsed_input_data = value

    @staticmethod
    def __fill_base_info(team_data: list, required_dict: dict) -> dict:
        for data in team_data:
            resource_id = data.get(TypesOfDataDict.resource_id)
            measurement = data.get(TypesOfDataDict.measurement)
            load = data.get(TypesOfDataDict.load)
            price = data.get(TypesOfDataDict.price)

            date_time = data.get(TypesOfDataDict.date_time)
            time_format = "%Y-%m-%d %H:%M:%S"
            if not type(date_time) is datetime.date:
                date_time_obj = datetime.datetime.strptime(date_time, time_format)
            else:
                date_time_obj = date_time

            required_dict.setdefault(resource_id, {}).setdefault(
                measurement, {}
            ).setdefault(TypesOfDataDict.load, [])
            required_dict[resource_id][measurement][TypesOfDataDict.load].append(
                int(load)
            )
            required_dict.setdefault(resource_id, {}).setdefault(measurement, {}).setdefault(
                TypesOfDataDict.price, int(price)
            )
            required_dict.setdefault(resource_id, {}).setdefault(
                measurement, {}
            ).setdefault(TypesOfDataDict.date_time, [])
            required_dict[resource_id][measurement][TypesOfDataDict.date_time].append(
                date_time_obj
            )
        return required_dict

    @staticmethod
    def calculate_average(list_of_values: list[int]):
        return sum(list_of_values) / len(list_of_values)

    @staticmethod
    def calculate_median(list_of_values: list[int]):
        quotient, remainder = divmod(len(list_of_values), 2)
        return (
            list_of_values[quotient]
            if remainder
            else sum(list_of_values[quotient - 1: quotient + 1]) / 2
        )

    def __fill_average(self, analytics_dict) -> dict:
        for resource_id, measurements in analytics_dict.items():
            for measurement, values in measurements.items():
                # list_of_loads = sorted(values.get(TypesOfDataDict.load))
                list_of_loads = analytics_dict[resource_id][measurement].pop(
                    TypesOfDataDict.load
                )

                average = self.calculate_average(list_of_loads)
                median = self.calculate_median(list_of_loads)
                analytics_dict[resource_id][measurement].update(
                    {TypesOfDataDict.average: average, TypesOfDataDict.median: median}
                )
        return analytics_dict

    @staticmethod
    def __last_date_measurement(analytics_dict) -> dict:
        for resource_id, measurements in analytics_dict.items():
            for measurement, values in measurements.items():
                list_of_date = analytics_dict[resource_id][measurement].pop(
                    TypesOfDataDict.date_time
                )
                last_date = sorted(list_of_date).pop()
                analytics_dict[resource_id][measurement].update(
                    {TypesOfDataDict.date_time: last_date}
                )
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
        if 0 <= median <= 30:
            status = TypesOfIntensity.low
        elif 30 < median <= 60:
            status = TypesOfIntensity.middle
        elif 60 < median <= 90:
            status = TypesOfIntensity.high
        elif median > 90:
            status = TypesOfIntensity.enormous
        else:
            raise ValueError(f"incorrect value: {median}, can't be lower that 0")
        return status

    @staticmethod
    def calculate_decision(load_type, intensity):
        if (intensity == TypesOfIntensity.low) or (
                intensity == TypesOfIntensity.middle and load_type == TypesOfLoad.decrease
        ):
            decision = "delete resource"
        elif (intensity == TypesOfIntensity.middle) and (
                load_type == TypesOfLoad.stable or load_type == TypesOfLoad.surges
        ):
            decision = "normal using"
        elif (intensity == TypesOfIntensity.high) and (
                load_type == TypesOfLoad.decrease or load_type == TypesOfLoad.stable
        ):
            decision = "normal using"
        elif (
                (load_type == TypesOfLoad.surges)
                and (intensity == TypesOfIntensity.high)
                or intensity == TypesOfIntensity.enormous
        ):
            decision = "extend resource"
        else:
            raise Exception(f"raw decision: {load_type} {intensity}")
        return decision

    def __fill_analytic_info(self, analytics_dict):
        for resource_id, measurements in analytics_dict.items():
            for measurement, values in measurements.items():
                average = analytics_dict[resource_id][measurement][
                    TypesOfDataDict.average
                ]
                median = analytics_dict[resource_id][measurement][
                    TypesOfDataDict.median
                ]

                load_type = self.calculate_load_type(average, median)
                analytics_dict[resource_id][measurement][
                    TypesOfDataDict.type_of_usage
                ] = load_type

                intensity = self.calculate_intensity(median)
                analytics_dict[resource_id][measurement][
                    TypesOfDataDict.intensity_of_usage
                ] = intensity

                decision = self.calculate_decision(load_type, intensity)
                analytics_dict[resource_id][measurement][
                    TypesOfDataDict.decision
                ] = decision
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
        analytics_dict = self.__last_date_measurement(analytics_dict)
        analytics_dict = self.__fill_analytic_info(analytics_dict)
        self.__analyzed_data.update({team_name_: analytics_dict})
        # pprint.pprint(analytics_dict)
        return analytics_dict

    def create_report(self, team_name):
        """
        Generating report based on analyzed data for provided team name.
        """
        team_data = self.__analyzed_data.get(team_name, None)
        if not team_data:
            team_data = self.calculate_data_analytic_for_team(team_name)
        print(
            f"|{TypesOfDataDict.resource_id}|{TypesOfDataDict.measurement}|{TypesOfDataDict.average}|"
            f"{TypesOfDataDict.median}|{TypesOfDataDict.type_of_usage}|{TypesOfDataDict.intensity_of_usage}|"
            f"{TypesOfDataDict.date_time}|{TypesOfDataDict.price}|{TypesOfDataDict.decision}|"
        )
        for resource_id, measurements in team_data.items():
            for measurement in measurements.keys():
                list_to_show = [
                    resource_id,
                    measurement,
                    str(team_data[resource_id][measurement][TypesOfDataDict.average]),
                    str(team_data[resource_id][measurement][TypesOfDataDict.median]),
                    str(
                        team_data[resource_id][measurement][
                            TypesOfDataDict.type_of_usage
                        ]
                    ),
                    str(
                        team_data[resource_id][measurement][
                            TypesOfDataDict.intensity_of_usage
                        ]
                    ),
                    str(team_data[resource_id][measurement][TypesOfDataDict.date_time]),
                    str(team_data[resource_id][measurement][TypesOfDataDict.price]),
                    str(team_data[resource_id][measurement][TypesOfDataDict.decision]),
                ]
                print(f"|{'|'.join(list_to_show)}|")

    def get_abnormal_decisions(self, team_name, required_decision=None):
        """
        :return: generator of entries where decision != "normal using"
        """
        if required_decision is None:
            required_decision = ["delete resource", "extend resource"]
        team_data = self.__analyzed_data.get(team_name)
        for resource_id, measurements in team_data.items():
            for measurement in measurements.keys():
                if team_data[resource_id][measurement][TypesOfDataDict.decision] in required_decision:
                    yield {
                        TypesOfDataDict.resource_id: resource_id,
                        TypesOfDataDict.measurement: measurement,
                        TypesOfDataDict.date_time: team_data[resource_id][measurement][TypesOfDataDict.date_time],
                        TypesOfDataDict.intensity_of_usage:
                            team_data[resource_id][measurement][TypesOfDataDict.intensity_of_usage],
                        TypesOfDataDict.type_of_usage:
                            team_data[resource_id][measurement][TypesOfDataDict.type_of_usage],
                        TypesOfDataDict.decision: team_data[resource_id][measurement][TypesOfDataDict.decision],
                        TypesOfDataDict.price: team_data[resource_id][measurement][TypesOfDataDict.price],
                    }

    def get_total_price(self, team_name):
        team_data = self.__analyzed_data.get(team_name)
        # result_list = []
        for resource_id, measurements in team_data.items():
            resource_list = []
            for measurement in measurements.keys():
                resource_list.append(team_data[resource_id][measurement][TypesOfDataDict.price])
            yield [resource_id, sum(resource_list)]
