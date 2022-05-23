from typing import Set, Dict, Iterator

from workers.storage_connector import PostgresClient
from workers.utils import ColumnTypeDB


class HostHandler:
    """
    Interlayer class between storage and client.
    """
    def __init__(self):
        self.psql = PostgresClient()

    def get_full_db(self):
        """
        :return: all entries from DB in raw format
        """
        return self.psql.get_info_from_db()

    def get_all_hosts(self, disabled: bool = False, user_id: str = "") -> Iterator[Dict]:
        """
        Method to get all hosts from DB
        :param disabled: if True - will be returned only hosts with STATUS = False
        :param user_id: if provided (internal username, not telegram id) will be returned hosts with such last modifier
        :return:
        """
        where_extension = {}
        if disabled:
            where_extension = {"where_extension_column": "status", "where_extension_pattern": "f"}
        for entry in self.psql.get_info_from_db(**where_extension):
            if not user_id or user_id == entry[ColumnTypeDB.last_modified_by_user]:
                yield {"hostname": entry[ColumnTypeDB.hostname],
                       "status": entry[ColumnTypeDB.status],
                       "last_modify_time": entry[ColumnTypeDB.last_modification_time],
                       "last_modified_by": entry[ColumnTypeDB.last_modified_by_user],
                       "comment": entry[ColumnTypeDB.comment],
                       "labels": entry[ColumnTypeDB.labels]}

    def get_all_hosts_by_label(self, label: str) -> Iterator[Dict]:
        """
        Method to get hosts from DB by some provided label
        :param label: label to find in db
        :return:
        """
        for entry in self.psql.get_info_from_db(
                where_extension_column="label", where_extension_pattern=label, like=True
        ):
            yield {"hostname": entry[ColumnTypeDB.hostname],
                   "status": entry[ColumnTypeDB.status],
                   "last_modify_time": entry[ColumnTypeDB.last_modification_time],
                   "last_modified_by": entry[ColumnTypeDB.last_modified_by_user],
                   "comment": entry[ColumnTypeDB.comment],
                   "labels": entry[ColumnTypeDB.labels]}

    def show_all_labels(self) -> Set:
        labels = set()
        for entry in self.psql.get_info_from_db(column="label"):
            for label in entry[0].split(","):
                labels.add(label.strip())
        return labels

    def show_all_users(self) -> Set:
        users = set()
        for entry in self.psql.get_info_from_db(column="last_modified_by"):
            users.add(entry[0])
        return users
