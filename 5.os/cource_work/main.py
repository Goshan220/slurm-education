import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path

from requests import get


class AccessController:
    def __init__(self, source: str):
        self.source = source
        self.__users_list = {}
        self.__ssh_dir = self.create_ssh_dir()

    @property
    def ssh_dir(self) -> Path:
        return self.__ssh_dir

    @property
    def authorized_keys(self) -> Path:
        return self.ssh_dir / "authorized_keys.txt"

    @staticmethod
    def __get_creds_as_query_params():
        return {
            "username": "user",
            "pass": "pass"
        }

    def do_request_to_server(self):
        response = get(url=self.source, params=self.__get_creds_as_query_params(), ).json()
        return response

    def read_data_from_file(self):
        with open(self.source) as file_:
            result = json.load(file_)
        return result

    @staticmethod
    def create_ssh_dir():
        if os.name == "nt":
            path_ = Path(os.environ.get("USERPROFILE")) / "slerm_ssh"
        elif os.name == "posix":
            path_ = Path("/root/.ssh/")
        else:
            raise Exception(f"Unexpected system {os.name}")

        try:
            path_.mkdir(exist_ok=True)
        except PermissionError:
            print("Permission denied to create folder, try to change parent folder access")
            try:
                path_.parent.chmod(0o777)
            except PermissionError:
                print("Can't change permission on parent dir")
                if os.name == "nt":
                    path_ = Path("C:\\slerm_ssh")
                else:
                    path_ = Path("/tmp/.ssh")
                print(f"Create temporary folder in {path_}")
                path_.mkdir(exist_ok=True)
        return path_

    @staticmethod
    def write_to_authorized_keys(file_path, entry: list, mode_: str = "a"):
        with open(file_path, mode_) as file_:
            file_.writelines(entry)

    @staticmethod
    def is_access_valid(date_from_json):
        date_time_obj = datetime.strptime(date_from_json, "%d-%m-%Y")
        return datetime.now() < date_time_obj

    def create_authorized_keys_file(self):
        if not self.authorized_keys.exists():
            with open(self.authorized_keys, "a"):
                pass

    def fill_authorized_keys(self, data: list, prev_iteration_keys: list = None):
        """
        :param data: json data from server
        :param prev_iteration_keys: list of valid users from last time when current function was called
        :return: current list of valid users to compare it in the future
        """
        self.create_authorized_keys_file()
        valid_keys = []
        for user in data:
            if self.is_access_valid(user.get("access_until")):
                print(f"fill_authorized_keys: access for user - {user.get('email')} is valid")
                valid_keys.append(str(user.get("rsa_pub_key") + "\n"))
            else:
                print(f"fill_authorized_keys: access for user - {user.get('email')} is not valid")

        if prev_iteration_keys == valid_keys:
            print("Nothing changed, there is no needs to update authorized_keys file")
        else:
            self.write_to_authorized_keys(self.authorized_keys, valid_keys, "w")
        return valid_keys

    def run_controller(self, frequency: int, debug: bool):
        breaker = 0
        prev_iteration_keys = None
        while True:
            if debug:
                if breaker == 5:
                    break
                breaker += 1

            if debug:
                data = self.read_data_from_file()
            else:
                data = self.do_request_to_server()

            prev_iteration_keys = self.fill_authorized_keys(data, prev_iteration_keys=prev_iteration_keys)

            print("#" * 50)
            time.sleep(frequency)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest="url", required=True, type=str, help="Enter URL of system control server")
    parser.add_argument(
        "-f", "--frequency", dest="frequency", required=True, type=int, help="Enter request frequency in minutes"
    )
    parser.add_argument("--debug", dest="debug", action="store_true", help="If this oprion enabled, --url will get path"
                                                                           "to local file (abspath)")
    args = parser.parse_args()

    AccessController(args.url).run_controller(frequency=args.frequency, debug=args.debug)


if __name__ == '__main__':
    main()
