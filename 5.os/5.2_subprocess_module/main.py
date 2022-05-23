import signal
import subprocess


def main():
    # subprocess.check_call(["ls", "-l", "-a"])
    # subprocess.check_call(["ls", "lll"])

    # ec = subprocess.call(["ls", "-l", "-a"], stdout=subprocess.DEVNULL)
    # print(ec)
    # ec = subprocess.call(["ls", "lll"], stdout=subprocess.DEVNULL)
    # print(ec)

    # output = subprocess.check_output(["ls", "-l", "-a"])
    # print(output.decode())


    # output = subprocess.check_output(["sed", "-e", "s/only golang.python/"],
    #                                  input="You can write k8s operator using only golang".encode())
    # print(output.decode())


    process = subprocess.Popen(["bahs", "echo_server.sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(process.poll())
    # process.terminate()
    # process.kill()
    # process.send_signal(signal.Signals.SIGINT)
    stdout, _ = process.communicate(input=b"one\ntwo\nthree\nfour")
    print(stdout.decode())
    print(process.decode())
    print(process.returncode)

    process.wait(timeout=3)


if __name__ == '__main__':
    main()
