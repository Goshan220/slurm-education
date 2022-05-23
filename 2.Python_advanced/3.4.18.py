import re


class MetricAgent:
    def __init__(self, server_ip: str, server_key: str):
        self.server_ip = server_ip
        self.server_key = server_key
        self.__number_collect_actions = 0
        self.__pull_period: int = 0
        self.__push_period: int = 0

    @staticmethod
    def __convert_period_to_sec(input_str):
        """
        :param input_str: строка для конвертации в секунды
        :return: результат конвертации в секундах
        """
        if "-" in input_str:
            raise ValueError("Отрицательное значение недопустимо!")
        split_ = re.findall(r'([0-9]*)([hms])', input_str)
        result = 0
        for i in split_:
            if i[1] == "h":
                result += int(i[0]) * 3600
            elif i[1] == "m":
                result += int(i[0]) * 60
            elif i[1] == "s":
                result += int(i[0])
            else:
                raise ValueError("Unrecognized symbol")
        return result

    @property
    def pull_period(self):
        return self.__pull_period

    @pull_period.setter
    def pull_period(self, new_period: str):
        self.__pull_period = self.__convert_period_to_sec(new_period)

    @property
    def push_period(self):
        return self.__push_period

    @push_period.setter
    def push_period(self, new_period):
        self.__push_period = self.__convert_period_to_sec(new_period)

    def collect_actions(self):
        self.__number_collect_actions += 1
        print(f"события сервера {self.server_ip} собраны. Следующий сбор через {self.pull_period} секунд")

    def push_actions(self):
        print(f"события сервера {self.server_ip} собраны отправлены на сервер сбора метрик. Следующиая отправка через "
              f"{self.push_period} секунд")

    def cache_reset(self):
        self.__number_collect_actions = 0
        print("кеш агента был очищен")

    def get_collected_actions_info(self):
        print(f"С сервера {self.server_ip} собрано {self.__number_collect_actions} событий")


class Prometheus(MetricAgent):
    @property
    def push_period(self):
        return super().push_period

    @push_period.setter
    def push_period(self, new_value):
        print("Вы не имеете возможности изменить push period")

    def push_actions(self):
        print(f"события сервера {self.server_ip} собраны отправлены по запросу от Prometheus")


class Carbon(MetricAgent):
    def __init__(self, server_ip: str, server_key: str, carbon_server_ip: str):
        super().__init__(server_ip=server_ip, server_key=server_key)
        self.carbon_server_ip = carbon_server_ip

    def push_actions(self):
        print(f"события сервера {self.server_ip} собраны отправлены в Carbon. "
              f"Следующая отправка через {self.push_period} секунд")
