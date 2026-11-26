import argparse
from datetime import date
from pathlib import Path

from input_utils import (
    read_date,
    read_menu_choice,
    read_non_empty,
    read_payment_method,
    read_positive_int,
)
from ledger import build_demo_ledger
from storage import load_ledger, save_ledger


DATA_PATH = Path(__file__).resolve().parent / "data" / "ledger.json"


def format_money(amount):
    sign = "-" if amount < 0 else ""
    grouped = f"{abs(amount):,}".replace(",", " ")
    return f"{sign}{grouped} руб."


def format_day(value):
    return value.strftime("%d.%m.%Y")


def print_account(account, as_of):
    print()
    print(f"Договор {account.contract_number}")
    print(account.full_name)
    print(f"Программа: {account.program}")
    print(f"Начислено: {format_money(account.total_charged)}")
    print(f"Оплачено: {format_money(account.total_paid)}")
    print(f"Задолженность: {format_money(account.debt)}")

    remainders = dict(account.unpaid_charges())
    print("Начисления:")
    if not account.charges:
        print("  нет")
    for charge in account.charges:
        remainder = remainders.get(charge, 0)
        print(
            f"  {charge.charge_id}. {charge.semester} | {charge.purpose} | "
            f"{format_money(charge.amount)} | срок {format_day(charge.due_date)} | "
            f"остаток {format_money(remainder)}"
        )

    print("Оплаты:")
    if not account.payments:
        print("  нет")
    for payment in account.payments:
        print(
            f"  {payment.payment_id}. {format_day(payment.paid_on)} | "
            f"{payment.method} | {format_money(payment.amount)}"
        )

    overdue = account.overdue(as_of)
    if overdue:
        print(f"Просрочено на {format_day(as_of)}:")
        for charge, remainder in overdue:
            print(f"  {charge.purpose}: {format_money(remainder)}")
    print()


def add_account(ledger):
    account = ledger.add_account(
        read_non_empty("ФИО студента: "),
        read_non_empty("Номер договора: "),
        read_non_empty("Программа обучения: "),
    )
    print(f"Договор {account.contract_number} добавлен.")


def add_charge(ledger):
    contract_number = read_non_empty("Номер договора: ")
    ledger.add_charge(
        contract_number,
        read_non_empty("Назначение начисления: "),
        read_positive_int("Сумма, руб.: "),
        read_date("Срок оплаты (ДД.ММ.ГГГГ): "),
        read_non_empty("Семестр: "),
    )
    print("Начисление добавлено.")


def add_payment(ledger):
    contract_number = read_non_empty("Номер договора: ")
    ledger.add_payment(
        contract_number,
        read_positive_int("Сумма, руб.: "),
        read_date("Дата оплаты (ДД.ММ.ГГГГ): "),
        read_payment_method(),
    )
    print("Оплата зарегистрирована. Реквизиты карты не сохраняются.")


def show_account(ledger, as_of):
    print_account(ledger.get(read_non_empty("Номер договора: ")), as_of)


def show_all(ledger, as_of):
    if not ledger.accounts:
        print("Журнал пуст.")
        return
    for account in ledger.accounts:
        print_account(account, as_of)


def show_debtors(ledger):
    debtors = ledger.debtors()
    if not debtors:
        print("Договоров с задолженностью нет.")
        return
    for account in debtors:
        print(
            f"{account.contract_number} | {account.full_name} | "
            f"{format_money(account.debt)}"
        )


def show_overdue(ledger, as_of):
    rows = ledger.overdue_rows(as_of)
    if not rows:
        print("Просроченных начислений нет.")
        return
    for account, charge, remainder in rows:
        print(
            f"{account.contract_number} | {account.full_name} | {charge.purpose} | "
            f"срок {format_day(charge.due_date)} | остаток {format_money(remainder)}"
        )


def run_menu(ledger, path, as_of=None):
    as_of = date.today() if as_of is None else as_of
    actions = {
        1: lambda: add_account(ledger),
        2: lambda: add_charge(ledger),
        3: lambda: add_payment(ledger),
        4: lambda: show_account(ledger, as_of),
        5: lambda: show_debtors(ledger),
        6: lambda: show_overdue(ledger, as_of),
        7: lambda: show_all(ledger, as_of),
        8: lambda: save_and_confirm(ledger, path),
    }
    while True:
        print("Учёт оплаты обучения")
        print("1. Добавить договор")
        print("2. Добавить начисление")
        print("3. Зарегистрировать оплату")
        print("4. Показать договор")
        print("5. Показать должников")
        print("6. Показать просроченные начисления")
        print("7. Показать все договоры")
        print("8. Сохранить")
        print("9. Выйти и сохранить")
        choice = read_menu_choice("Выберите действие: ", 1, 9)
        if choice == 9:
            save_ledger(ledger, path)
            print(f"Журнал сохранён: {path}")
            break
        try:
            actions[choice]()
        except ValueError as error:
            print(error)


def save_and_confirm(ledger, path):
    save_ledger(ledger, path)
    print(f"Журнал сохранён: {path}")


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Учебный учёт оплаты обучения")
    parser.add_argument("--demo", action="store_true", help="открыть журнал с учебными договорами")
    parser.add_argument("--data", default=str(DATA_PATH), help="путь к файлу журнала")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    path = Path(args.data)
    if args.demo:
        ledger = build_demo_ledger()
        print("Открыт демонстрационный журнал. Это не данные реальных студентов.")
    else:
        ledger = load_ledger(path)
        if ledger.accounts:
            print(f"Загружен журнал: {path}")
        else:
            print("Новый пустой журнал.")
    run_menu(ledger, path)


if __name__ == "__main__":
    main()
