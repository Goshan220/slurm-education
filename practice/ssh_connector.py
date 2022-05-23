import paramiko


class SSHConnector:
    def __init__(self):
        self.__key = None
        self.__read_key()

    def __read_key(self):
        with open("I:\\slerm\\key_openssh_server.txt") as __file:
            self.__key = __file.readline()

    def run_db_data_generator(self, seed: int = 1):
        with paramiko.SSHClient() as ssh_client:
            ssh_client.load_system_host_keys()
            ssh_client.connect(
                "localhost",
                2222,
                username="service_user",
                password=self.__key
            )

            # put file on server
            ftp_client = ssh_client.open_sftp()
            ftp_client.put(
                "I:\\slerm\\pythonforops\\3.Client_modules\\final_practice_helpers\\monitoring_module.py",
                "/tmp/monitoring_module.py"
            )
            # я узнал, что monitoring_module лежит бинарём в /usr/bin и был обескуражен...
            # решил не удалять этот кусок, т.к. потратил время на поиск того как копировать файлы по ssh
            ftp_client.close()

            # change rights on file and run it
            _, stdout, stderr = ssh_client.exec_command(
                f"chmod +x /tmp/monitoring_module.py && python3 /tmp/monitoring_module.py {seed}"
            )
            err = stderr.read().decode()
            if err:
                print(err)
