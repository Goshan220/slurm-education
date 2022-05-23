EXPERIENCE = 6


def log_function_using(functor):

    def decorate():
        print("Функция была вызвана")
        functor()
        print("Функция была завершена")

    return decorate


def inc_experience():
    global EXPERIENCE
    EXPERIENCE += 1


def main():
    print(EXPERIENCE)
    log_function_using(inc_experience)()
    print(EXPERIENCE)


if __name__ == '__main__':
    main()
