import datetime

from errbot import BotPlugin, botcmd
from errbot.backends.telegram_messenger import TelegramPerson

from workers.host_handler import HostHandler
from workers.utils import ALERT_CHANNEL, ALERT_LABEL_THRESHOLD, convert_id, generate_report, send_email, \
    MonitoringException


class MonitoringPlugin(BotPlugin):
    def __init__(self, bot, name):
        super().__init__(bot, name)
        self.hh = HostHandler()

    @botcmd()
    def show_full_db(self, msg, args):
        """
        To debug
        """
        for entry in self.hh.get_full_db():
            self.send(msg.frm, str(entry))

    @botcmd
    def all_disabled(self, msg, args):
        for entry in self.hh.get_all_hosts(disabled=True):
            self.send_templated(msg.frm, template_name="disabled_host", template_parameters=entry)

    @botcmd
    def disabled(self, msg, args):
        """
        Command returns all DISABLED hosts by username
        """
        user_id = args or str(msg.frm)
        try:
            for entry in self.hh.get_all_hosts(disabled=True, user_id=convert_id(user_id=user_id)):
                self.send_templated(msg.frm, template_name="disabled_host", template_parameters=entry)
        except MonitoringException as e:
            self.send(msg.frm, "Provided user was not found in list of disabled hosts")

    def get_summary_by_label(self, label):
        host_counter = 0
        enabled_counter = 0
        for entry in self.hh.get_all_hosts_by_label(label):
            host_counter += 1
            if entry["status"]:
                enabled_counter += 1
        percent = int(enabled_counter / host_counter * 100)
        return host_counter, enabled_counter, percent

    @botcmd(template="label_summary")
    def status_by_label(self, msg, args):
        if not args:
            labels = ", ".join(self.hh.show_all_labels())
            self.send(msg.frm, labels)
            self.send(msg.frm, "Please provide valid label from list above")
            return
        host_counter, enabled_counter, percent = self.get_summary_by_label(args)
        return {
            "label": args,
            "total": host_counter,
            "enabled": enabled_counter,
            "percent": percent
        }

    def activate(self) -> None:
        """
        Scheduler of current plugin methods.
        label_alerting: will be called 3 times with 5 sec interval.
        send_report: will be called 1 times with 10 sec interval.
        """
        super().activate()
        self.start_poller(interval=5, method=self.alert_labels_to_channel, times=3)
        self.start_poller(interval=10, method=self.generate_and_send_report, times=1)

    def alert_labels_to_channel(self):
        """
        Method automatically send alerts to TG chanel if number of hosts less than ALERT_LABEL_THRESHOLD by each label
        """
        all_labels = self.hh.show_all_labels()
        for label in all_labels:
            host_counter, enabled_counter, percent = self.get_summary_by_label(label)
            if percent < ALERT_LABEL_THRESHOLD:
                message_options = {
                    "label": label,
                    "host_counter": host_counter,
                    "enabled_counter": enabled_counter,
                    "percent": percent
                }
                self.send_templated(
                    TelegramPerson(ALERT_CHANNEL),
                    template_name="label_alert",
                    template_parameters=message_options
                )

    def generate_and_send_report(self):
        """
        Method automatically generate and send HTML-report about all Disabled hosts sorted by user.
        """
        options = {}
        users = self.hh.show_all_users()
        for user in users:
            list_of_hosts = self.hh.get_all_hosts(disabled=True, user_id=user)
            if not list_of_hosts:
                continue
            options.setdefault("users", []).append({"username": user, "hosts": list_of_hosts})
        options["generation_time"] = datetime.datetime.now()
        path_to_html_report = generate_report(options)
        send_email(html_report_path=path_to_html_report)
