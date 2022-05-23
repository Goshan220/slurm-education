import re
from typing import Mapping
from errbot import BotPlugin, Message, botcmd, arg_botcmd, re_botcmd
from trello import TrelloClient


class TaskCreater(BotPlugin):

    def get_configuration_template(self) -> Mapping:
        return {
            "TRELLO_API_KEY": "changeme",
            "TRELLO_API_SECRET": "changeme",
        }

    @re_botcmd(pattern="^Создай задачу (?P<name>.*?):\s*(?P<desc>.*?) на (?<department>(?:SRE|DevOps))$", template="task_created")
    def create_task_regexply(self, msg, matcher: re.Match):
        return self.__create_task_at_trello(matcher.group("name"), matcher.group("desc"), matcher.group("department"))

    @arg_botcmd("name", type=str, template="task_created")
    @arg_botcmd("--desc", type=str, dest="description", template="task_created")
    @arg_botcmd("--dep", type=str, dest="description", default="SRE", template="task_created")
    def create_task(self, msg, name, description, department):
        return self.__create_task_at_trello(name, desc=description, dep=department)

    @botcmd(template="task_created")
    def create_task_directly(self, msg, args):
        return self.__create_task_at_trello(args)

    def __create_task_at_trello(self, name, desc="", dep=None):
        if self.config is None:
            return "You should fill config before run command!"
        trello_client = TrelloClient(
            api_key=self.config["TRELLO_API_KEY"],
            api_secret = self.config["TRELLO_API_SECRET"]
        )

        board = trello_client.list_boards()[0]
        selected_list = board.list_lists()[1 if dep == "SRE" else 0]
        selected_list.add_card(name=name, desc=desc)

        return {
            "name": name,
            "board_name": board.name,
            "list_name": selected_list.name,
        }

    def callback_message(self, message: Message) -> None:
        if any([trigger in message.body.lower() for trigger in ["эй пес", "err"]]):
            self.send(message.to, "На месте")
