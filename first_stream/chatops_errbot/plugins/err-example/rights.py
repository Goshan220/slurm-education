from json import load
from re import IGNORECASE, MULTILINE, Match
from os import path
from errbot import BotPlugin, arg_botcmd, re_botcmd
import paramiko


class Rights(BotPlugin):

    def __init__(self, bot, name=None):
        super().__init__(bot, name)
        current_dir = path.dirname(path.realpath(__file__))
        with open(path.join(current_dir, "config.json")) as configfile:
            self._plugin_config = load(configfile)

        self._key = paramiko.RSAKey.from_private_key_file(path.join(current_dir, "id_rsa"),
                                                          password=self._plugin_config["KEY_PASS"])

    @arg_botcmd("--accessed_user", dest="accessed_user", type=str)
    @arg_botcmd("--key", dest="key", type=str)
    @arg_botcmd("--user", dest="user", type=str)
    def access_create(self, _, accessed_user, key, user):
        with paramiko.SSHClient() as ssh_client:
            ssh_client.load_system_host_keys()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh_client.connect("sbox.slurm.io", 22, "s011274", pkey=self._key)
            authorized_keys_path = f"/home/{accessed_user[1:3]}/{accessed_user[3:5]}/{accessed_user}/.ssh/authorized_keys"
            with ssh_client.open_sftp() as sftp_client:
                self.log.info(f"Open file {authorized_keys_path}")
                with sftp_client.open(authorized_keys_path, "a") as authorized_keys_file:
                    authorized_keys_file.write(f"{key} {user}\n")
        yield "Success"
        yield f"Access *granted* for {user} through authorized hosts of {accessed_user}!"

    @re_botcmd(pattern="^Can you delete key of (.*?) on (.*?)$", flags=IGNORECASE | MULTILINE)
    def access_delete(self, _, macher: Match):
        user = macher.group(1)
        accessed_user = macher.group(2)

        with paramiko.SSHClient() as ssh_client:
            ssh_client.load_system_host_keys()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh_client.connect("sbox.slurm.io", 22, "s011274", pkey=self._key)
            authorized_keys_path = f"/home/{accessed_user[1:3]}/{accessed_user[3:5]}/{accessed_user}/.ssh/authorized_keys"
            with ssh_client.open_sftp() as sftp_client:
                self.log.info(f"Open file {authorized_keys_path}")
                with sftp_client.open(authorized_keys_path, "r") as authorized_keys_file:
                    content = authorized_keys_file.readlines()
                with sftp_client.open(authorized_keys_path, "w") as authorized_keys_file:
                    for line in content:
                        if user not in line:
                            authorized_keys_file.write(line)
        return f"Key for {user} access through {accessed_user} *was deleted*!"

    def callback_message(self, message) -> None:
        if any(trigger in message.body.lower() for trigger in ["как добавить ключ", "как получить доступ"]):
            self.send(message.to,
                      "You can use command !access create")

