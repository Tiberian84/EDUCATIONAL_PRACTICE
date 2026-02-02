#❌✅
from datetime import datetime

"""
Функции для запроса даты рождения у пользователя
"""


def get_birth_date():
    """Запрашиваем у пользователя по очереди день, месяц, год рождения"""
    while True:
        #Запрашиваем день
        while True:
            try:
                day = int(input("Введите день рождения (1-31): "))
                if 1 <= day <= 31:
                    break
                else:
                    print("❌ День должен быть от 1 до 31. Попробуйте ещё раз.")
            except ValueError:
                print("❌ Введите число!")
        
        #Запрашиваем месяц
        while True:
            try:
                month = int(input("Введите месяц рождения (1-12): "))
                if 1 <= month <= 12:
                    break
                else:
                    print("❌ Месяц должен быть от 1 до 12. Попробуйте ещё раз.")
            except ValueError:
                print("❌ Введите число!")

        #Запрашиваем год
        while True:
            try:
                year = int(input("Введите год рождения (напр. 2000): "))
                if 1900 <= year <= 2026:
                    break
                else:
                    print("❌ Год должен быть в разумных пределах(1900-2026).")
            except ValueError:
                print("❌ Введите число!")
        try:
            datetime(year, month, day)
            return day, month, year
        except ValueError:
            print("\n❌ Нет такой даты! (например, 31 апреля или 29 февраля в невисокосный год)")
            print("😊 Попробуй ещё раз!\n")