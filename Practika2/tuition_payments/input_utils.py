from datetime import datetime

from ledger import PAYMENT_METHODS


def read_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Поле не может быть пустым.")


def read_positive_int(prompt):
    while True:
        raw = input(prompt).strip().replace(" ", "")
        if raw.isdigit() and int(raw) > 0:
            return int(raw)
        print("Введите целое число больше нуля, без копеек.")


def read_date(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            return datetime.strptime(raw, "%d.%m.%Y").date()
        except ValueError:
            print("Введите дату в формате ДД.ММ.ГГГГ.")


def read_payment_method():
    print("Способ оплаты:")
    for index, method in enumerate(PAYMENT_METHODS, start=1):
        print(f"{index}. {method}")
    while True:
        raw = input("Выберите способ: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(PAYMENT_METHODS):
            return PAYMENT_METHODS[int(raw) - 1]
        print("Выберите номер из списка. Номер карты вводить не нужно.")


def read_menu_choice(prompt, minimum, maximum):
    while True:
        raw = input(prompt).strip()
        if raw.isdigit() and minimum <= int(raw) <= maximum:
            return int(raw)
        print(f"Введите номер от {minimum} до {maximum}.")
