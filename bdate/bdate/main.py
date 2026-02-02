#✅📅🎂
from datetime import datetime, date
from calendar import isleap

import input_utils

def get_weekday(day, month, year):
    """Определяет день недели по дате"""
    birth_date = datetime(year, month, day)
    weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    return weekdays[birth_date.weekday()]


def get_leap_year_status(year):
    """Возвращает 'високосный' или 'невисокосный' для указанного года."""
    return "високосный" if isleap(year) else "невисокосный"

def is_leap_year_manual(year):
    """Проверяет високосность года вручную (без calendar.isleap)."""
    return (year % 4 == 0 and year % 100 !=0) or year % 400 == 0

def calculate_age(day, month, year):
    """Возвращает текущий возраст."""
    birth_date = date(year, month, day)
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day): 
        age -= 1
    return age

def get_year_word(age):
    """Возвращает правильное склонение год, года, лет"""
    if age % 100 in range(11, 15):
        return "лет"
    else:
        last_digit = age % 10

        if last_digit == 1:
            return "год"
        elif last_digit in range(2,5):
            return "года"
        else:
            return "лет"
        
def print_date_big(day, month, year):
    """
    Вывод в консоль даты рождения пользователя в формате дд мм гггг, где цифры прорисованы звёздочками (*), как на электронном табло:
    """
    #  ***     *    *****   *****   *   *   *****   *****   *****   *****   *****       *
    # *   *   **        *       *   *   *   *       *           *   *   *   *   *      * 
    # *   *    *    *****    ****   *****   *****   *****     ***   *****   *****     *  
    # *   *    *    *           *       *       *   *   *       *   *   *       *    *   
    #  ***    ***   *****   *****       *   *****   *****       *   *****   *****   *    
    date_str = f"{day:02d}.{month:02d}.{year}"
    digit_patterns = {
    "0": [" *** ", "*   *", "*   *", "*   *", " *** "],
    "1": ["  *  ", " **  ", "  *  ", "  *  ", " *** "],
    "2": ["*****", "    *", "*****", "*    ", "*****"],
    "3": ["*****", "    *", " ****", "    *", "*****"],
    "4": ["*   *", "*   *", "*****", "    *", "    *"],
    "5": ["*****", "*    ", "*****", "    *", "*****"],
    "6": ["*****", "*    ", "*****", "*   *", "*****"],
    "7": ["*****", "    *", "  ***", "    *", "    *"],
    "8": ["*****", "*   *", "*****", "*   *", "*****"],
    "9": ["*****", "*   *", "*****", "    *", "*****"],
    ".": ["    *", "   * ", "  *  ", " *   ", "*    "]
    }

    print()
    for row in range(5):
        line_parts = []
        for i in date_str:
            line_parts.append(digit_patterns[i][row])
        print(" ".join(line_parts))
    print()

if __name__ == "__main__":

    day, month, year = input_utils.get_birth_date()
    weekday = get_weekday(day, month, year)
    leap_status = "високосный" if is_leap_year_manual(year) else "невисокосный"
    age = calculate_age(day, month, year)

    print(f"\n✅ Ваша дата рождения: {day:02d}.{month:02d}.{year}")
    print(f"📅 День недели: {weekday}")
    #print(f"📅 {year} - {get_leap_year_status(year)}")
    print(f"📅 {year} - {leap_status}")
    print(f"🎂 Вам {age} {get_year_word(age)}")
    print_date_big(day, month, year)
    
