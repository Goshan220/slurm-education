from collections import deque, namedtuple, defaultdict, Counter

def main():
    names = ["Denis", "Denis", "Valentine", "Nadya", "Alexander"]

    # frozenset
    frozen_names = frozenset(names)
    print(frozen_names)
    
    # deque
    deque_names = deque(names)
    last_value = deque_names.pop()
    deque_names.appendleft(last_value)
    print(deque_names)

    # namedtuple
    CourseCreator = namedtuple("CourseCreators", ("speaker", "methodist", "tech_support", "PO", "PMM"))
    creators = CourseCreator(speaker="Denis", methodist="Denis", tech_support="Alexander", PO="Valentine", PMM="Nadya")
    print(creators)
    print(creators.methodist)

    # defaultdict

    def default_name():
        return "Slurm"

    names_dict = defaultdict(default_name)
    names_dict["PMM"] = "Nadya"
    names_dict["Speaker"]
    print(names_dict)

    # Counter
    word_counter = Counter()
    word_counter["Оператор"] += 1
    word_counter["Оператор"] += 2
    word_counter["Операция"] += 3
    word_counter["Операция"] += 2
    word_counter["Операция"] += 3
    word_counter["Множество"] += 1
    word_counter["Множество"] += 1
    word_counter["Множество"] += 1
    word_counter["Множество"] += 30
    word_counter["Словарь"] += 13098
    print(word_counter)
    print(word_counter.most_common(2))


if __name__ == '__main__':
    main()
