from os import getenv
import paramiko


def main() -> None:
    key = paramiko.RSAKey.from_private_key_file("/home/beantorong/.ssh/id_rsa", password=getenv("KEY_PASS"))
    with paramiko.SSHClient() as ssh_client:
        ssh_client.load_system_host_keys()
        # ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh_client.connect(hostname="localhost", port=2222,
                           username="service_user", pkey=key)
        stdin, stdout, stderr = ssh_client.exec_command("ls -la /")
        print(stdout.read().decode("utf-8"))

        stdin, stdout, stderr = ssh_client.exec_command("echotest")

        stdin.write("Hello!\n")
        stdin.flush()
        print(stdout.readline())
        stdin.write("Hello world!\n")
        stdin.flush()
        print(stdout.readline())

        stdin, stdout, stderr = ssh_client.exec_command("task_generator")
        print(stderr.read())
        print(stdout.read())

        with ssh_client.open_sftp() as sftp_client:
            sftp_client.get(remotepath="/usr/bin/task_generator", localpath="./task_generator_2")
            try:
                sftp_client.put(localpath="./main.py", remotepath="/main.py")
            except PermissionError:
                sftp_client.put(localpath="./main.py", remotepath="/tmp/main.py")

            with sftp_client.open("/tmp/main.py") as main_py_file:
                print(main_py_file.read().decode())

            try:
                sftp_client.rename(oldpath="/tmp/main.py", newpath="/tmp/main_old.py")
            except OSError:
                sftp_client.remove(path="/tmp/main_old.py")
                sftp_client.rename(oldpath="/tmp/main.py", newpath="/tmp/main_old.py")

            sftp_client.truncate(path="/tmp/main_old.py", size=0)

            print(sftp_client.getcwd())
            sftp_client.chdir("/")
            print(sftp_client.getcwd())

            sftp_client.chmod("/tmp/main_old.py", 777)


if __name__ == '__main__':
    main()
