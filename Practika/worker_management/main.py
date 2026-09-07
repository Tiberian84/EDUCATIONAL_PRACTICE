from worker import Worker
from datetime import datetime

worker_list = []
worker_list.append(Worker("Иванов И.И.", "Менеджер", 100000, 2020))
worker_list.append(Worker("Петров П.П.", "Разработчик", 80000, 2021))
worker_list.append(Worker("Сидоров С.С.", "Дизайнер", 70000, 2022))
worker_list.append(Worker("Кузнецов А.А.", "Аналитик", 60000, 2023))
worker_list.append(Worker("Васильев С.С.", "Менеджер", 100000, 2020))
worker_list.append(Worker("Петров П.П.", "Аналитик", 60000, 2023))

def add_worker():
    print("\033[94mВыберите способ добавления работника\033[0m")
    print("\033[94m1. Вручную\033[0m")
    print("\033[94m2. Менеджер\033[0m")
    print("\033[94m3. Разработчик\033[0m")
    print("\033[94m4. Дизайнер\033[0m")
    print("\033[94m5. Аналитик\033[0m")
    choice = int(input("Выберите действие: "))
    if choice == 1:
        add_worker_manual()
    elif choice == 2:
        add_manager()
    elif choice == 3:
        add_developer()
    elif choice == 4:
        add_designer()
    elif choice == 5:
        add_analyst()

def add_worker_manual():
    print("\033[94mВведите данные для добавления работника\033[0m")
    fio = input("Введите ФИО: ")
    position = input("Введите должность: ")
    salary = int(input("Введите зарплату: "))
    hire_year = int(input("Введите год найма: "))
    worker_list.append(Worker(fio, position, salary, hire_year))
    print(f"\033[92m {position} {fio} добавлен\033[0m")

def add_manager():
    print("\033[94mВведите данные для добавления менеджера\033[0m")
    fio = input("Введите ФИО: ")
    hire_year = int(input("Введите год найма: "))
    worker_list.append(Worker.manager(fio, hire_year))
    print(f"\033[92mМенеджер {fio} добавлен\033[0m")

def add_developer():
    print("\033[94mВведите данные для добавления разработчика\033[0m")
    fio = input("Введите ФИО: ")
    hire_year = int(input("Введите год найма: "))
    worker_list.append(Worker.developer(fio, hire_year))
    print(f"\033[92mРазработчик {fio} добавлен\033[0m")

def add_designer():
    print("\033[94mВведите данные для добавления дизайнера\033[0m")
    fio = input("Введите ФИО: ")
    hire_year = int(input("Введите год найма: "))
    worker_list.append(Worker.designer(fio, hire_year))
    print(f"\033[92mДизайнер {fio} добавлен\033[0m")


def add_analyst():
    print("\033[94mВведите данные для добавления аналитика\033[0m")
    fio = input("Введите ФИО: ")
    hire_year = int(input("Введите год найма: "))
    worker_list.append(Worker.analyst(fio, hire_year))
    print(f"\033[92mАналитик {fio} добавлен\033[0m")

def delete_worker():
    fio = input("Введите ФИО: ")
    print("Введено:", repr(fio))
    for worker in worker_list:
        if worker.fio == fio:
            worker_list.remove(worker)
            print("\033[92mРаботник {fio} удален\033[0m")
            break
    else:
        print("\033[91mРаботник {fio} не найден\033[0m")

def update_worker():
    fio = input("Введите ФИО: ")
    for worker in worker_list:
        if worker.fio == fio:
            worker.update(
                position=input("Введите должность: "),
                salary=int(input("Введите зарплату: ")),
                hire_year=int(input("Введите год найма: "))
            )
            print("\033[92mРаботник изменен\033[0m")
            break
    else:
        print("\033[91mРаботник не найден\033[0m")

def show_all_workers():
    for worker in worker_list:
        worker.show()

def show_workers_with_experience():
    current_year = datetime.now().year
    found = False
    experienced_workers = []
    experience = int(input("Введите стаж работы: "))
    for worker in worker_list:
        if worker.hire_year < current_year - experience:
            found = True
            experienced_workers.append(worker)
    if found:
        print("\033[92mНайдены работники с таким стажем работы:\033[0m")
        for worker in experienced_workers:
            print(worker.fio)
    if not found:
        print("\033[91mРаботники с таким стажем не найдены\033[0m")

def main():
    while True:
        print("\033[94m1. Добавить работника\033[0m")
        print("\033[94m2. Удалить работника\033[0m")
        print("\033[94m3. Изменить работника\033[0m")
        print("\033[94m4. Показать всех работников\033[0m")
        print("\033[94m5. Показать работника превышающих следующий стаж работы:\033[0m")
        print("\033[94m6. Выйти\033[0m")
        choice = int(input("Выберите действие: "))
        if choice == 1:
            add_worker()
        elif choice == 2:
            delete_worker()
        elif choice == 3:
            update_worker()
        elif choice == 4:
            show_all_workers()
        elif choice == 5:
            show_workers_with_experience()
        elif choice == 6:
            break
        else:
            print("\033[91mНеверный выбор\033[0m")

if __name__ == "__main__":
    main()