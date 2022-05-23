def generate_sequence(max_value=5000000):
    for number in range(0, max_value + 1):
        yield number


def add_two(value):
    return str(value + 2)


def main():
    values = {add_two(number): number for number in generate_sequence() if number % 2112 == 0}
    print(values)


if __name__ == '__main__':
    main()
