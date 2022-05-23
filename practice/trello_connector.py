import datetime
import random

from requests import Session

from practice.utils import TypesOfDataDict


class TrelloConnector:
    api_url = "https://api.trello.com/1"

    def __init__(self, board_name: str = "course_work"):
        self.__api_key = None
        self.__api_token = None
        self.__read_api_key_token()

        self.__board_name = board_name
        self.__board_id = None

        self.__board_lists = {}
        self.__labels = {}
        self.__session = Session()

    def __read_api_key_token(self):
        with open("I:\\slerm\\key_trello.txt") as __file:
            self.__api_key = __file.readline()[:-1]  # [:-1] is workaround because I don't know how
            self.__api_token = __file.readline()[:-1]  # to read from file keys correctly, without /n

    def __get_creds_as_query_params(self):
        return {
            "key": self.__api_key,
            "token": self.__api_token,
        }

    @property
    def board_name(self):
        return self.__board_name

    @board_name.setter
    def board_name(self, new_board_name):
        """
        You can specify board name before calling 'prepare_environment' or 'prepare_board' with 'prepare_lists'
        """
        self.__board_name = new_board_name

    @property
    def board_lists(self):
        return self.__board_lists

    @property
    def labels(self):
        return self.__labels

    @property
    def session(self):
        return self.__session

    def prepare_board(self):
        """
        Getting board ID from Trello
        """
        boards = self.session.get(
            url=f"{self.api_url}/members/me/boards",
            params=self.__get_creds_as_query_params(),
        ).json()
        for board in boards:
            if board["name"] == self.board_name:
                self.__board_id = board["id"]

    def prepare_lists(self):
        """
        Get lists of board by current board_id
        """
        lists = self.session.get(
            url=f"{self.api_url}/boards/{self.__board_id}/lists",
            params=self.__get_creds_as_query_params(),
        ).json()
        for list_ in lists:
            self.__board_lists.update({list_["name"]: list_["id"]})

    def get_labels(self):
        labels = self.session.get(
            url=f"{self.api_url}/boards/{self.__board_id}/labels",
            params=self.__get_creds_as_query_params(),
        ).json()
        for label in labels:
            if label["name"]:
                self.__labels.update({label["name"]: label["id"]})

    def get_cards_in_a_list(self, args):
        params = {
            **self.__get_creds_as_query_params(),
        }
        response = self.session.get(
            url=f"{self.api_url}/lists/{args['idList']}/cards",
            params=params,
        )
        return response.json()

    def create_label(self, name: str):
        """
        Create label with name
        :param name: name of label
        """
        colors = ["yellow", "purple", "blue", "red", "green", "black", "orange", "sky", "pink", "lime"]
        params = {
            **self.__get_creds_as_query_params(),
            "name": name,
            "color": colors[random.randrange(0, 10)],
        }
        response = self.session.post(
            url=f"{self.api_url}/boards/{self.__board_id}/labels",
            params=params,
        ).json()
        self.__labels.update({response["name"]: response["id"]})
        return response["id"]

    def __create_task(self, args):
        params = {**self.__get_creds_as_query_params(), **args}
        response = self.session.post(url=f"{self.api_url}/cards", params=params)
        print(response.text)

    def prepare_environment(self):
        self.prepare_board()
        self.prepare_lists()
        self.get_labels()

    def create_task_trello(self, task_description: dict):
        if task_description[TypesOfDataDict.decision] == "delete resource":
            name = (
                f"Отказаться от использования ресурса {task_description[TypesOfDataDict.resource_id]} по измерению "
                f"{task_description[TypesOfDataDict.measurement]}"
            )
        else:
            name = (
                f"Увеличить квоты ресурса {task_description[TypesOfDataDict.resource_id]} по измерению "
                f"{task_description[TypesOfDataDict.measurement]}"
            )
        description = (
            f"тип использования: {task_description[TypesOfDataDict.type_of_usage]}, "
            f"интенсивность использования: {task_description[TypesOfDataDict.intensity_of_usage]}"
        )

        due = task_description[TypesOfDataDict.date_time] + datetime.timedelta(days=14)
        label_id = self.labels.get(task_description["team_name"], None)
        if not label_id:
            label_id = self.create_label(task_description["team_name"])

        query = {
            "name": name,
            "idList": self.board_lists.get("TODO"),
            "desc": description,
            "idLabels": [label_id],
            "due": due,
        }
        exists_tasks = self.get_cards_in_a_list(query)
        for _task in exists_tasks:
            if _task["name"] == query["name"]:
                print("INFO: such ticket already exists, skip...")
                return
        self.__create_task(query)
