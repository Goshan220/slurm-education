def main():
    with open('file.txt', 'w+') as my_file:
        for i in range(10):
            my_file.write(f"test {i} \n")
        my_file.flush()
        print(my_file.readline())
        print('-' * 5)
        print(my_file.readlines())
        print('-' * 5)
        print(my_file.readable())
        print(my_file.writable())
        print('-' * 5)
        print(my_file.name)
        print('-' * 5)
        print(my_file.encoding)
        print('-' * 5)
        my_file.truncate(8)
    print(my_file.closed)


if __name__ == "__main__":
    main()
