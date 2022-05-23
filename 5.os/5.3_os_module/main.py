import os


def main():
    print(os.name)
    print(os.uname())

    print(os.getlogin())
    print(os.environ.get("HOME"))
    print(os.getenv("HOME"))
    print(os.getenv("HOME_2", "/root"))

    print(os.getcwd())
    os.chdir("../")
    print(os.getcwd())
    os.chdir("slurm_python_for_ops")

    print(os.listdir("."))

    os.mkdir("test")
    os.chdir("test")
    os.mkdir("nested")
    with open("test_file", "w") as test_file:
        test_file.write("Hello python and os module")

    os.chmod("test_file", 0o777, follow_symlinks=True)
    print(os.listdir("."))
    os.rename("test_file", "test_file_2")
    print(os.listdir("."))
    # os.remove("test_file_2")
    # print(os.listdir("."))

    files = [path for path in os.listdir() if os.path.isfile(path)]
    dirs = [path for path in os.listdir() if os.path.isdir(path)]

    print("* files", files)
    print("* dirs", dirs)

    for file_path in files:
        os.remove(file_path)

    for dir_path in dirs:
        os.rmdir(dir_path)

    # for delete_nested(file_path, dir_path):
    #     for file_path in files:
    #         os.remove(file_path)
    #
    #     for dir_path in dirs:
    #         os.rmdir(dir_path)
    #         os.chdir(dir_path)
    #
    #         files = [path for path in os.listdir() if os.path.isfile(path)]
    #         dirs = [path for path in os.listdir() if os.path.isdir(path)]
    #
    #         delete_nested(files, dir_path)

    os.chdir("../")
    os.rmdir("test")
    print(os.listdir("."))

    os.makedirs("test/nested/nested")
    os.renames("test/nested/nested", "test/nested_2/nested_3")
    # os.removedirs("test/nested_2/nested_3")

    print(os.path.exists("test/nested_2"))
    print(os.path.exists("test/nested_4"))
    if not os.path.exists("test/nested_4"):
        os.makedirs("test/nested_4")

    print(os.path.isfile("main.py"), os.path.isfile("test"))
    print(os.path.isdir("main.py"), os.path.isdir("test"))

    print(os.path.abspath("main.py"))
    print(os.path.abspath("test"))

    print(os.path.basename("/home/beantorong/PycharmProjects/slurm_python_for_ops/main.py"))
    print(os.path.basename("/home/beantorong/PycharmProjects/slurm_python_for_ops/test"))

    print(os.path.dirname("PycharmProjects/slurm_python_for_ops/main.py"))
    print(os.path.dirname("PycharmProjects/slurm_python_for_ops/test"))

    print(os.path.getsize("main.py"))

    # os.rmdir("test")


if __name__ == '__main__':
    main()
