
def get_input(list_to_extend: list):
    """
    в input программа принимает:
     1) числа по одному через enter
     2) строки вида - (100;132;123;211)
     3) строки вида - [3, 6]
    для выхода из ввода, ввести пустую строку
    :return:
    """
    while True:
        input_ = input("Введите число или последовательность: ")
        _slice = []
        if input_ == "":
            return _slice
        elif input_[0] == "(" and input_[-1] == ")":
            list_to_extend.extend(input_[1:-1].split(";"))
        elif input_[0] == "[" and input_[-1] == "]":
            _slice.extend(input_[1:-1].split(","))
            return _slice
        else:
            list_to_extend.append(int(input_))


def convert_data_to_int_and_sort(data_list: list):
    for value in range(len(data_list)):
        data_list[value] = int(data_list[value])
    return sorted(data_list)


def get_frequency(data_list: list):
    frequency_dict = {}
    for value in data_list:
        curr_value = frequency_dict.get(value)
        if curr_value:
            frequency_dict[value] += 1
        else:
            frequency_dict[value] = 1
    print(f"frequency = {frequency_dict}")


def calculating(data_list: list):
    data_list = convert_data_to_int_and_sort(data_list=data_list)
    print(f"data_list: {data_list}")

    sum_of_data_list_values = 0
    for value in range(len(data_list)):
        sum_of_data_list_values += data_list[value]

    average = sum_of_data_list_values / len(data_list)
    print(f"average: {average}")

    quotient, remainder = divmod(len(data_list), 2)
    median = int(data_list[quotient]) if remainder else sum((data_list[quotient - 1:quotient + 1])) / 2
    print(f"median: {median}")

    deviation_25 = (median-(median/100)*25, median, median+(median/100)*25)

    if average < deviation_25[0]:
        print("Происходят снижения")
    elif deviation_25[2] < average:
        print("Происходят скачки")
    else:
        print("Нагрузка стабильна")


if __name__ == '__main__':
    rps_values = [
        5081, '17184', 10968, 9666, '9102', 12321, '10617', 11633, 5035, 9554, '10424', 9378, '8577', '11602', 14116,
        '8066', '11977', '8572', 9685, 11062, '10561', '17820', 16637, 5890, 17180, '17511', '13203', 13303, '7330',
        7186, '10213', '8063', '12283', 15564, 17664, '8996', '12179', '13657', 15817, '16187', '6381', 8409, '5177',
        17357, '10814', 6679, 12241, '6556', 12913, 16454, '17589', 5292, '13639', '7335', '11531', '14346', 7493,
        15850, '12791', 11288
    ]

    slice_ = get_input(list_to_extend=rps_values)
    print(f"PRS values: {rps_values}")

    print("Инфо по всем значениям rps_values")
    full_data_list = rps_values.copy()
    calculating(data_list=full_data_list)
    get_frequency(data_list=full_data_list)
    if slice_:
        sliced_data_list = rps_values[int(slice_[0]):int(slice_[1])]
        print("Инфо по подвыборке из rps_values")
        calculating(data_list=sliced_data_list)
        get_frequency(data_list=sliced_data_list)
