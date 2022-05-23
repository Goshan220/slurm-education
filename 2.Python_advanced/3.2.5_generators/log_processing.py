def read_file_generator(file_name):
    with open(file_name) as log_file:
        for row in log_file:
            yield row


def main():
    for row in read_file_generator("log_2021_06_06.txt"):
        if row.lower().startswith("error"):
            print(row)


if __name__ == '__main__':
    main()
