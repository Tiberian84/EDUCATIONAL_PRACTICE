class Worker:
    def __init__(self, fio="", position="", salary=0, hire_year=0):
        self.fio = fio
        self.position = position
        self.salary = salary
        self.hire_year = hire_year
    
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
        print(self.fio, self.position, self.salary, self.hire_year)

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
