from datetime import datetime


class Worker:
    def __init__(self, fio=None, position=None, salary=None, hire_year=None):
        self.__fio = ""
        self.__position = ""
        self.__salary = 0
        self.__hire_year = 0

        if fio is not None:
            self.fio = fio
        if position is not None:
            self.position = position
        if salary is not None:
            self.salary = salary
        if hire_year is not None:
            self.hire_year = hire_year

    @property
    def fio(self):
        return self.__fio

    @fio.setter
    def fio(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("ФИО не может быть пустым")
        self.__fio = value.strip()

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Должность не может быть пустой")
        self.__position = value.strip()

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("Зарплата должна быть целым числом")
        if value < 0:
            raise ValueError("Зарплата не может быть отрицательной")
        self.__salary = value

    @property
    def hire_year(self):
        return self.__hire_year

    @hire_year.setter
    def hire_year(self, value):
        current_year = datetime.now().year
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("Год найма должен быть целым числом")
        if value < 1900 or value > current_year:
            raise ValueError(f"Год найма должен быть в диапазоне от 1900 до {current_year}")
        self.__hire_year = value
    
    @classmethod
    def manager(cls, fio, hire_year):
        return cls(fio, "Менеджер", 100000, hire_year)
    
    @classmethod
    def developer(cls, fio, hire_year):
        return cls(fio, "Разработчик", 80000, hire_year)
    
    @classmethod
    def designer(cls, fio, hire_year):
        return cls(fio, "Дизайнер", 70000, hire_year)
    
    @classmethod
    def analyst(cls, fio, hire_year):
        return cls(fio, "Аналитик", 60000, hire_year)

    def show(self):
        print(self.__fio, self.__position, self.__salary, self.__hire_year)

    def update(self, fio=None, position=None, salary=None, hire_year=None):
        if fio is not None:
            self.fio = fio
        if position is not None:
            self.position = position
        if salary is not None:
            self.salary = salary
        if hire_year is not None:
            self.hire_year = hire_year

    def __del__(self):
        pass
