from practice.db_connector import DBManager
from practice.local_server_connector import LocalServerManager
from practice.sto_worker import STOWorker
from practice.ssh_connector import SSHConnector
from practice.trello_connector import TrelloConnector
from practice.utils import PracticeException, TypesOfDataDict


def run_collecting_data(source: str = "localhost") -> dict:
    """
    Start collecting data from local server (module 2) or from Database with paramico (module 3)
    :param source: can be "localhost" - module 2, "database" - module 3
    :return: firstly prepared data from source
    """
    if source == "http":
        connector = LocalServerManager()
        return connector.parse_raw_input_to_dict()
    elif source == "database":
        connector = DBManager()
        return connector.parse_data_from_db()
    else:
        raise PracticeException("Unexpected source value, expected: 'localhost' or 'database'")


def main_module_3(data_source: str):
    """
    main function for module 3
    :param data_source: will be used to understand what the source of input data will be: 'http' or 'database'
    """
    # filling database with values
    # docker_connector = SSHConnector()
    # docker_connector.run_db_data_generator(seed=2)  # it works but commented to stop putting new data to DB

    trello_connector = TrelloConnector(board_name="test_desk")
    trello_connector.prepare_environment()

    # get base input from db or localhost and initialize main data worker with data
    sto_worker = STOWorker(run_collecting_data(data_source))

    for team_name in sto_worker.parsed_input_data.keys():
        print("\n" * 2 + team_name)

        # sto_worker.calculate_data_analytic_for_team(team_name)  # possible to run method but create_report will
        sto_worker.create_report(team_name)  # prepare data if currently its empty

        for entry in sto_worker.get_abnormal_decisions(team_name):
            entry.update({"team_name": team_name})
            trello_connector.create_task_trello(entry)


def main_module_4(data_source):
    """
    main function for module 3
    """
    if data_source != "http":
        raise PracticeException("This module works only with local service via http")

    # get base input from localhost and initialize main data worker with data
    sto_worker = STOWorker(run_collecting_data(data_source))
    for team_name in sto_worker.parsed_input_data.keys():
        print("\n" * 2 + team_name)
        print("General report:")
        sto_worker.create_report(team_name)

        print("\nTotal price:")
        for resource in sto_worker.get_total_price(team_name):
            print(f"resource: {resource[0]} price: {resource[1]}")

        print("\nPrice for decision - delete resource")
        for entry in sto_worker.get_abnormal_decisions(team_name, required_decision=["delete resource"]):
            print(
                f"{entry[TypesOfDataDict.resource_id]}: {entry[TypesOfDataDict.measurement]}: {entry[TypesOfDataDict.price]}")
    exit(0)


if __name__ == '__main__':
    while True:
        input_ = input("Please, type source of data: 'http' or 'database', or type 'exit' - to exit from program. "
                       "Default ['exit']: ").lower()
        if input_ == "" or input_ == 'exit':
            exit(2)  # 2 just to understand that it was interrupted by user input
        if input_ == "http" or input_ == "database":
            # main_module_3(input_)
            main_module_4(input_)
        else:
            print("source of data incorrect, please, follow the instructions:")
