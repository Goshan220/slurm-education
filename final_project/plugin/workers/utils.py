import datetime
import smtplib
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional

from jinja2 import Template

ALERT_CHANNEL = "channel_id"  # TODO here is channel id for alerts
ALERT_LABEL_THRESHOLD = 40
NOTIFICATION_LIST = "some_email@company.com"
EMAIL_SENDER = "internal_user@company.com"
MAIL_SERVER = "localhost"  # mailserver.company.com


class MonitoringException(Exception):
    pass


class ColumnTypeDB:
    __id = 0
    hostname = 1
    status = 2
    comment = 3
    last_modification_time = 4
    last_modified_by_user = 5
    labels = 6


def convert_id(user_id: str, convert_to_tg: bool = False):
    id_map = {"75051276": "igor", "000333": "alena", "111000": "stas"}  # TODO add this to storage
    if convert_to_tg:
        for id_, user_name in id_map.items():
            if user_name == user_id:
                return id_
        raise MonitoringException(f"User {user_id} not found")
    else:
        id_ = id_map.get(user_id, None)
        if id_:
            return id_
        raise MonitoringException(f"User {user_id} not found")


def generate_report(options: dict) -> Path:
    """
    :param options: options for jinja generator. Example of options structure for HTML generator:
        options = {"users": [
            {"username": "ivan",
             "hosts": [{"hostname": "some_host1", "status": "false"}, {"hostname": "some_host2", "status": "true"}]},
            {"username": "igor",
             "hosts": [{"hostname": "some_host4", "status": "true"}, {"hostname": "some_host6", "status": "false"}]}
        ]}
    :return: Path to report saved locally
    """
    with open(Path("workers", "report_template.html"), "r") as file_:
        template_str = file_.read()

    template = Template(template_str, trim_blocks=True, lstrip_blocks=True)
    html_output = template.render(**options)

    Path("output").mkdir(exist_ok=True)

    output_path = Path("output", f"monitoring_report_{datetime.datetime.now().date()}.html")
    with open(output_path, "w") as file_:
        file_.write(html_output)
    return output_path


def send_email(html_report_path: Optional[Path] = None):
    """
    to debug: python -m smtpd -c DebuggingServer -n localhost:1025
    """
    smtp_obj = smtplib.SMTP(MAIL_SERVER, 1025)

    with open(html_report_path, "r") as fp:
        msg = MIMEText(fp.read())

    msg['Subject'] = f"Host status reporting: {datetime.datetime.now()}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = NOTIFICATION_LIST

    try:
        smtp_obj.set_debuglevel(1)
        smtp_obj.sendmail(EMAIL_SENDER, NOTIFICATION_LIST, msg.as_string())
        print(msg.as_string())
    except smtplib.SMTPException as e:
        print(f"Unable to send message: {e}")
    finally:
        smtp_obj.quit()
