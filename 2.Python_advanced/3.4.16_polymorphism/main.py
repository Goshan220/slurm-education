class Slurmik:

    specialization = "K8S grandmaster"

    @staticmethod
    def tell_about_specialization():
        print("Я не могу иметь специализацию")

    """ Существо слёрмик """

    def __init__(self, name: str, profession: str, experience: int):
        """
        Конструктор
        :param name: Имя слёрмика
        :param profession: профессия слёрмика
        :param experience: стаж слёрмика (в годах)
        """
        self._name = name
        self._profession = profession
        self._experience = experience

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_value):
        if not isinstance(new_value, str) or len(new_value) <= 0:
            raise ValueError("Имя должно быть непустой строкой")
        self._name = new_value

    def say_hello(self):
        """
        Приветствует программиста
        :return:
        """
        print(f"Привет! Я слёрмик {self._name}. Я {self._profession}, мой стаж {self._experience} лет.")

    def __change_experience(self, new_value: int, reason: str):
        """
        Смена стажа
        :param new_value: новый стаж (в годах)
        :param reason: причина смены стажа
        :return:
        """
        print(f"Слёрмик {self._name} сменил стаж {self._experience} на {new_value}. Причина: {reason}")
        self._experience = new_value

    def convert_experience_to_mercury_year(self):
        """
        Переезд на Меркурий и смена стажа на меркурианские года
        :return:
        """
        self.__change_experience(self._experience * (365 // 88), "Переезд на Меркурий")


class SlurmikDev(Slurmik):

    def __init__(self, name: str, profession: str, experience: int, favorite_lang: str):
        """
        Конструктор
        :param name: Имя слёрмика
        :param profession: профессия слёрмика
        :param experience: стаж слёрмика (в годах)
        :param favorite_lang: любимый ЯП
        """
        super().__init__(name, profession, experience)
        self.__fav_lang = favorite_lang

    def write_program(self, code_row_count):
        """
        Написание программы
        :param code_row_count: количество строк кода
        """
        print(f"Я {self.name} и я пишу программу из {code_row_count} строк кода на {self.__fav_lang}")

    def say_hello(self):
        """
        Приветствует программиста
        :return:
        """
        print(f"Привет! Я слёрмик {self._name}. Я {self._profession}, мой стаж программирования {self._experience} лет.")


def main():
    slurmik_vanya = Slurmik("Иван", "DevOps engineer", 14)
    slurmik_masha = Slurmik("Маша", "DevOps engineer", 10)
    slurmik_dima = SlurmikDev("Влад", "Программист", 6, "Ruby")

    for slurmik in [slurmik_vanya, slurmik_masha, slurmik_dima]:
        slurmik.say_hello()


if __name__ == '__main__':
    main()
