class Slurmik():
    """ Существо слёрмик """

    specialization = "K8S grandmaster"

    @staticmethod
    def tell_about_specialization():
        print("Я не могу иметь специализацию")


    def __init__(self, name: str, profession: str, experience: int):
        """
        Конструктор
        :param name: Имя слёрмика
        :param profession: профессия слёрмика
        :param experience: стаж слёрмика (в годах)
        """
        self.__name = name
        self.__profession = profession
        self.__experience = experience

    def say_hello(self):
        """
        Приветствует программиста
        :return:
        """
        print(f"Привет! Я слёрмик {self.__name}. Я {self.__profession}, мой стаж {self.__experience} лет.")

    def __change_experience(self, new_value: int, reason: str):
        """
        Смена стажа
        :param new_value: новый стаж (в годах)
        :param reason: причина смены стажа
        :return:
        """
        print(f"Слёрмик {self.__name} сменил стаж {self.__experience} на {new_value}. Причина: {reason}")
        self.__experience = new_value

    def convert_experience_to_mercury_year(self):
        """
        Переезд на Меркурий и смена стажа на меркурианские года
        :return:
        """
        self.__change_experience(self.__experience * (365 // 88), "Переезд на Меркурий")


def main():
    slurmik_vanya = Slurmik("Иван", "DevOps engineer", 14)
    slurmik_masha = Slurmik("Маша", "DevOps engineer", 10)

    slurmik_masha.specialization = "AWS"
    slurmik_masha.specialization_2 = "Kafka"

    slurmik_masha.tell_about_specialization()
    slurmik_vanya.tell_about_specialization()

    print("-" * 30)

    print(slurmik_masha.specialization)
    print(slurmik_masha.specialization_2)
    print(slurmik_vanya.specialization)


if __name__ == '__main__':
    main()
