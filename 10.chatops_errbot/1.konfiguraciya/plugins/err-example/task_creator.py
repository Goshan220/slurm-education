from typing import Mapping
from errbot import BotPlugin, botcmd
from trello import TrelloClient


class TaskCreater(BotPlugin):

    def get_configuration_template(self) -> Mapping:
        return {
            "TRELLO_API_KEY": "changeme",
            "TRELLO_API_SECRET": "changeme",
        }

    @botcmd
    def create_task_directory(self, msg, args):
        if self.config is None:
            return "You should fill config before run command!"
        task_name = "Test task"
        trello_client = TrelloClient(
            api_key=self.config["TRELLO_API_KEY"],
            api_secret = self.config["TRELLO_API_SECRET"]
        )

        board = trello_client.list_boards()[0]
        first_list = board.list_lists()[0]
        first_list.add_card(name=task_name, desc="This is test task")

        return f"Task \"{task_name}\" was created on board \"{board.name}\" at list \"{first_list.name}\""
