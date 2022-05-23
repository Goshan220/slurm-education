from json import load
from random import choice
from os import getenv

import paramiko
from requests import Session


class Credentials:
    """ Credentials для доступа к Trello по REST API """
    def __init__(self):
        self.__api_token = getenv("TRELLO_API_TOKEN")
        self.__api_key = getenv("TRELLO_API_KEY")

    def get_creds_as_query_params(self):
        return {
            "key": self.__api_key,
            "token": self.__api_token,
        }


class TrelloBoard:
    """ Доска Trello"""

    def __init__(self, name: str, board_id: str, creds: Credentials):
        self.__name = name
        self.__id = board_id
        self.__columns = None
        self.__labels = None
        self.__creds = creds

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @property
    def columns(self):
        return self.__columns

    @property
    def labels(self):
        return self.__labels

    def __get_board_root_entity(self, session: Session, entity: str) -> dict:
        """
        Получение корневой сущности определенной доски Trello
        :param session: сессия requests
        :param entity: сущность
        :return: отображение имени колонки на её id
        """
        columns = session.get(f"https://api.trello.com/1/boards/{self.__id}/{entity}",
                              params=self.__creds.get_creds_as_query_params()).json()
        return {column["name"]: column["id"] for column in columns}

    def get_board_columns(self, session: Session) -> None:
        """
            Получение колонок определенной доски Trello
            :param session: сессия requests
            :return: отображение имени колонки на её id
            """
        self.__columns = self.__get_board_root_entity(session, "lists")

    def get_board_labels(self, session: Session) -> None:
        """
        Получение меток определенной доски Trello
        :param session: сессия requests
        :return: отображение имени метки на её id
        """
        self.__labels = self.__get_board_root_entity(session, "labels")

    def __create_root_entity(self, session: Session, entity_details: dict, entity: str) -> dict:
        """
        Создание задачи (карточки) на доске Trello
        :param session: сессия requests
        :param entity_details: детали задачи (название, описание, ID колонки)
        :param entity: сущность
        :return: отображение имени сущности на ID
        """
        params = {
            **self.__creds.get_creds_as_query_params(),
            **entity_details,
        }
        return session.post(f"https://api.trello.com/1/{entity}", params=params).json()

    def create_task(self, session: Session, task_details: dict):
        self.__create_root_entity(session, task_details, "cards")

    def create_label(self, session: Session, label_details: dict):
        label = self.__create_root_entity(session, label_details, "labels")
        self.__labels[label["name"]] = label["id"]


def get_boards(session: Session, creds: Credentials) -> list[TrelloBoard]:
    """
    Получение досок Trello и колонок в них
    :param session: сессия requests
    :param creds: параметры доступа к Trello
    :return: отображение имени доски на её id и колонки
    """
    boards = session.get("https://api.trello.com/1/members/me/boards",
                         params=creds.get_creds_as_query_params()).json()
    return [TrelloBoard(board["name"], board["id"], creds) for board in boards]


def get_tasks_from_generator() -> list:
    """
    Получение списка задач от генератора на удаленном сервере
    :return: список задач
    """
    key = paramiko.RSAKey.from_private_key_file("/home/beantorong/.ssh/id_rsa", password=getenv("KEY_PASS"))
    with paramiko.SSHClient() as ssh_client:
        ssh_client.load_system_host_keys()
        ssh_client.connect("localhost", 2222, "service_user", pkey=key)
        _, stdout, stderr = ssh_client.exec_command("task_generator 2")
        err = stderr.read().decode()
        if err:
            print(err)
            exit(1)
        return load(stdout)


def get_label_id(board: TrelloBoard, checked_label_name: str):
    for label_name, label_id in board.labels.items():
        if label_name == checked_label_name:
            return label_id


def main():
    LABELS_COLORS = ["yellow", "purple", "blue", "red", "green", "orange", "black", "sky", "pink", "lime"]
    trello_creds = Credentials()
    trello_session = Session()

    board = get_boards(trello_session, trello_creds)[0]
    board.get_board_columns(trello_session)
    board.get_board_labels(trello_session)
    column = board.columns["Нужно сделать"]

    for task in get_tasks_from_generator():
        used_labels = []
        for task_label in task["lables"] or []:
            label_id = get_label_id(board, task_label)
            if label_id is None:
                board.create_label(trello_session, {
                    "name": task_label,
                    "color": choice(LABELS_COLORS),
                    "idBoard": board.id
                })
                label_id = get_label_id(board, task_label)
            used_labels.append(label_id)

        task_details = {
            "name": task["name"],
            "desc": task["desc"],
            "due": task["due"],
            "idList": column,
            "idLabels": ",".join(used_labels),
        }
        board.create_task(trello_session, task_details)

    trello_session.close()


if __name__ == '__main__':
    main()

