import re
from typing import Mapping
from errbot import BotPlugin, Message, botcmd, re_botcmd
from errbot.backends.telegram_messenger import TelegramPerson
from trello import TrelloClient
import redis


class DevOpsBot(BotPlugin):
    def __init__(self, bot, name):
        super().__init__(bot, name)
        self.r = RedisClient()

    def get_configuration_template(self) -> Mapping:
        return {
            "TRELLO_API_KEY": "changeme",
            "TRELLO_API_SECRET": "changeme",
        }

    def _is_user_devops(self, userid):
        _devops_id_list = self.r.connection.lrange("devops", 0, -1)
        for _id in _devops_id_list:
            if _id == userid:
                return True
        return False

    @botcmd()
    def add_devops(self, msg, args):
        if not self._is_user_devops(str(msg.frm)):
            return "Sorry you are not a DevOps"
        self.r.connection.lpush("devops", args)
        return f"User {args} was added to DevOps team"

    @botcmd()
    def remove_devops(self, msg, args):
        if not self._is_user_devops(str(msg.frm)):
            return "Sorry you are not a DevOps"
        _devops_id_list = self.r.connection.lrange("devops", 0, -1)
        for i in range(len(_devops_id_list)):
            self.r.connection.lpop("devops")
            if not _devops_id_list[i] == args:
                self.r.connection.rpush("devops", _devops_id_list[i])
            else:
                return f"User {args} was removed from DevOps team"
        return f"User {args} not found in DevOps team list"

    @re_botcmd(pattern="вопрос: (?P<question>.*?)$", template="request_created")
    def q(self, msg, matcher: re.Match):
        """
        Бот, вопрос: в чём смысл жизни?
        :return: Вопрос "в чём смысл жизни?" был успешно получен
        """
        question = matcher.group("question")
        _id = f"question:{self.r.connection.dbsize() + 1}"
        data = {"userid": str(msg.frm), "question": question, "done": "False"}
        self.r.connection.hset(_id, mapping=data)
        return {"question": question}

    @botcmd()
    def all(self, msg, args):
        if not self._is_user_devops(str(msg.frm)):
            return "Sorry you are not a DevOps"
        _keys = self.r.connection.keys("question:*")
        _keys.sort(key=lambda x: float(x[9:]))
        for key in _keys:
            self.send(msg.frm, str(self.r.connection.hvals(key)))
        return

    @botcmd()
    def next(self, msg, args):
        if not self._is_user_devops(str(msg.frm)):
            return "Sorry you are not a DevOps"
        key = self.__searh_in_db("question", 2, "False")
        self.send(msg.frm, f"Next in progress task number: {key}")
        self.send(msg.frm, f"User: {self.r.connection.hvals(key)[0]}")
        self.send(msg.frm, f"Question: {self.r.connection.hvals(key)[1]}")
        self.r.connection.hset(key, mapping={"done": "in_progress"})
        return

    @botcmd()
    def done(self, msg, args):
        if not self._is_user_devops(str(msg.frm)):
            return "Sorry you are not a DevOps"
        key = self.__searh_in_db("question", 2, "in_progress")
        self.send(msg.frm, f"Task is done")
        self.send(TelegramPerson(self.r.connection.hvals(key)[0]), args)
        self.r.connection.hset(key, mapping={"done": "True"})
        return

    @botcmd()
    def newtask(self, msg, args):
        if not self._is_user_devops(str(msg.frm)):
            return "Sorry you are not a DevOps"
        key = self.__searh_in_db("question", 2, "in_progress")
        res = self.__create_task_at_trello(key, desc=self.r.connection.hvals(key)[1], dep="SRE")
        self.send(msg.frm, f"Ticket created")
        self.send(
            TelegramPerson(
                self.r.connection.hvals(key)[0]), f"Ticket number {res['name']} was created on {res['board_name']}"
        )
        self.r.connection.hset(key, mapping={"done": "True"})

    def __searh_in_db(self, key_name, hval_numb, hval_value):
        _keys = self.r.connection.keys(f"{key_name}:*")
        _keys.sort(key=lambda x: float(x[len(key_name) + 1:]))
        for key in _keys:
            if self.r.connection.hvals(key)[hval_numb] == hval_value:
                return key

    def __create_task_at_trello(self, name, desc="", dep=None):
        if self.config is None:
            return "You should fill config before run command!"
        trello_client = TrelloClient(
            api_key=self.config["TRELLO_API_KEY"],
            api_secret=self.config["TRELLO_API_SECRET"]
        )

        board = trello_client.list_boards()[0]
        selected_list = board.list_lists()[int(dep == "SRE")]
        selected_list.add_card(name=name, desc=desc)

        return {
            "name": name,
            "board_name": board.name,
            "list_name": selected_list.name,
        }

    def callback_message(self, message: Message) -> None:
        if any([trigger in message.body.lower() for trigger in ["эй раб"]]):
            self.send(message.frm, "В суд go?")
            self.send(message.frm, str(message.frm))


class RedisClient:
    def __init__(self):
        self.__connection = None

    @property
    def connection(self):
        if self.__connection is None:
            self.__connection = redis.Redis(charset="utf-8", decode_responses=True)
        return self.__connection
