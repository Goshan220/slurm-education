def log_function_using(functor):

    def decorate(val):
        print("Функция была вызвана")
        result = functor(val)
        print(f"Функция была завершена. Результат {result}")
        return result

    return decorate


@log_function_using
def inc_experience(old_value):
    return old_value + 1


def main():
    exp = 6
    exp = inc_experience(exp)
    print(exp)


if __name__ == '__main__':
    main()
