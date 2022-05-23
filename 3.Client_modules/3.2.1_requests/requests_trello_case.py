from os import getenv
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


def get_boards(session: Session, creds: Credentials) -> dict:
    """
    Получение досок Trello и колонок в них
    :param session: сессия requests
    :param creds: параметры доступа к Trello  
    :return: отображение имени доски на её id и колонки 
    """
    boards = session.get("https://api.trello.com/1/members/me/boards",
                         params=creds.get_creds_as_query_params()).json()
    return {board["name"]: {
        "id": board["id"],
        "columns": get_board_columns(session, creds, board["id"])
    } for board in boards}


def get_board_columns(session: Session, creds: Credentials, board_id: str) -> dict:
    """
    Получение колонок определенной доски Trello 
    :param session: сессия requests
    :param creds: параметры доступа к Trello  
    :param board_id: ID доски Trello
    :return: отображение имени колонки на её id  
    """
    columns = session.get(f"https://api.trello.com/1/boards/{board_id}/lists",
                          params=creds.get_creds_as_query_params()).json()
    return {column["name"]: column["id"] for column in columns}


def create_task(session: Session, creds: Credentials, column_id: str, task_details: dict):
    """
    Создание задачи (карточки) на доске Trello
    :param session: сессия requests
    :param creds: параметры доступа к Trello 
    :param column_id: ID колонки
    :param task_details: детали задачи (название, описание)
    :return: 
    """
    params = {
        **creds.get_creds_as_query_params(),
        **task_details,
        "idList": column_id
    }
    result = session.post("https://api.trello.com/1/cards", params=params)
    print(result.status_code)
    print(result.text)


def main():
    trello_creds = Credentials()
    trello_session = Session()
    boards = get_boards(trello_session, trello_creds)
    for board_name, board_info in boards.items():
        print(f"Доска {board_name}")
        print("Колонки: ")
        for column_name in board_info["columns"].keys():
            print(column_name)
    task_details = {
        "name": input("Введите название задачи: "),
        "desc": input("Введите описание задачи: ")
    }

    entered_column_name = input("Введите название колонки: ")

    used_column_id = None
    for board_name, board_info in boards.items():
        for column_name, column_id in board_info["columns"].items():
            if column_name == entered_column_name:
                used_column_id = column_id
                break
        else:
            continue
        break

    create_task(trello_session, trello_creds, used_column_id, task_details)
    trello_session.close()


if __name__ == '__main__':
    main()
