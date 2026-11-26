from datetime import date, datetime


PAYMENT_METHODS = ("СБП", "Банковская карта", "Банковский перевод")


def _require_text(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} не может быть пустым")
    return value.strip()


def _require_positive_int(value, field_name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field_name} должна быть целым числом")
    if value <= 0:
        raise ValueError(f"{field_name} должна быть больше нуля")
    return value


def _require_date(value, field_name):
    if not isinstance(value, date) or isinstance(value, datetime):
        raise ValueError(f"{field_name} должна быть датой")
    return value


class Charge:
    """Начисление по договору на обучение."""

    def __init__(self, charge_id, purpose, amount, due_date, semester):
        if isinstance(charge_id, bool) or not isinstance(charge_id, int) or charge_id < 1:
            raise ValueError("Номер начисления должен быть положительным целым числом")
        self.charge_id = charge_id
        self.purpose = _require_text(purpose, "Назначение начисления")
        self.amount = _require_positive_int(amount, "Сумма начисления")
        self.due_date = _require_date(due_date, "Дата срока оплаты")
        self.semester = _require_text(semester, "Семестр")

    def to_dict(self):
        return {
            "charge_id": self.charge_id,
            "purpose": self.purpose,
            "amount": self.amount,
            "due_date": self.due_date.isoformat(),
            "semester": self.semester,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["charge_id"],
            data["purpose"],
            data["amount"],
            date.fromisoformat(data["due_date"]),
            data["semester"],
        )


class Payment:
    """Факт оплаты. Номер карты и другие платёжные реквизиты не хранятся."""

    def __init__(self, payment_id, amount, paid_on, method):
        if isinstance(payment_id, bool) or not isinstance(payment_id, int) or payment_id < 1:
            raise ValueError("Номер оплаты должен быть положительным целым числом")
        self.payment_id = payment_id
        self.amount = _require_positive_int(amount, "Сумма оплаты")
        self.paid_on = _require_date(paid_on, "Дата оплаты")
        if method not in PAYMENT_METHODS:
            allowed = ", ".join(PAYMENT_METHODS)
            raise ValueError(f"Способ оплаты должен быть одним из: {allowed}")
        self.method = method

    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "amount": self.amount,
            "paid_on": self.paid_on.isoformat(),
            "method": self.method,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["payment_id"],
            data["amount"],
            date.fromisoformat(data["paid_on"]),
            data["method"],
        )


class StudentAccount:
    """Лицевой счёт студента по договору на обучение."""

    def __init__(self, full_name, contract_number, program):
        self.full_name = _require_text(full_name, "ФИО студента")
        self.contract_number = _require_text(contract_number, "Номер договора")
        self.program = _require_text(program, "Программа обучения")
        self._charges = []
        self._payments = []

    @property
    def charges(self):
        return list(self._charges)

    @property
    def payments(self):
        return list(self._payments)

    @property
    def total_charged(self):
        return sum(charge.amount for charge in self._charges)

    @property
    def total_paid(self):
        return sum(payment.amount for payment in self._payments)

    @property
    def debt(self):
        return self.total_charged - self.total_paid

    def add_charge(self, purpose, amount, due_date, semester):
        charge = Charge(self._next_charge_id(), purpose, amount, due_date, semester)
        self._charges.append(charge)
        return charge

    def add_payment(self, amount, paid_on, method):
        payment = Payment(self._next_payment_id(), amount, paid_on, method)
        self._payments.append(payment)
        return payment

    def unpaid_charges(self):
        """Распределяет оплаты по начислениям от раннего срока к позднему."""
        money_left = self.total_paid
        unpaid = []
        ordered = sorted(self._charges, key=lambda charge: (charge.due_date, charge.charge_id))
        for charge in ordered:
            covered = min(charge.amount, money_left)
            money_left -= covered
            remainder = charge.amount - covered
            if remainder > 0:
                unpaid.append((charge, remainder))
        return unpaid

    def overdue(self, as_of):
        as_of = _require_date(as_of, "Дата проверки")
        return [
            (charge, remainder)
            for charge, remainder in self.unpaid_charges()
            if charge.due_date < as_of
        ]

    def to_dict(self):
        return {
            "full_name": self.full_name,
            "contract_number": self.contract_number,
            "program": self.program,
            "charges": [charge.to_dict() for charge in self._charges],
            "payments": [payment.to_dict() for payment in self._payments],
        }

    @classmethod
    def from_dict(cls, data):
        account = cls(data["full_name"], data["contract_number"], data["program"])
        account._charges = [Charge.from_dict(item) for item in data.get("charges", [])]
        account._payments = [Payment.from_dict(item) for item in data.get("payments", [])]
        return account

    def _next_charge_id(self):
        if not self._charges:
            return 1
        return max(charge.charge_id for charge in self._charges) + 1

    def _next_payment_id(self):
        if not self._payments:
            return 1
        return max(payment.payment_id for payment in self._payments) + 1


class Ledger:
    """Журнал договоров на обучение."""

    def __init__(self):
        self._accounts = {}

    @property
    def accounts(self):
        return list(self._accounts.values())

    def add_account(self, full_name, contract_number, program):
        number = _require_text(contract_number, "Номер договора")
        if number in self._accounts:
            raise ValueError(f"Договор {number} уже есть в журнале")
        account = StudentAccount(full_name, number, program)
        self._accounts[number] = account
        return account

    def get(self, contract_number):
        number = _require_text(contract_number, "Номер договора")
        account = self._accounts.get(number)
        if account is None:
            raise ValueError(f"Договор {number} не найден")
        return account

    def add_charge(self, contract_number, purpose, amount, due_date, semester):
        return self.get(contract_number).add_charge(purpose, amount, due_date, semester)

    def add_payment(self, contract_number, amount, paid_on, method):
        return self.get(contract_number).add_payment(amount, paid_on, method)

    def debtors(self):
        return [account for account in self.accounts if account.debt > 0]

    def overdue_rows(self, as_of):
        rows = []
        for account in self.accounts:
            for charge, remainder in account.overdue(as_of):
                rows.append((account, charge, remainder))
        return rows

    def to_dict(self):
        return {"accounts": [account.to_dict() for account in self.accounts]}

    @classmethod
    def from_dict(cls, data):
        ledger = cls()
        for item in data.get("accounts", []):
            account = StudentAccount.from_dict(item)
            if account.contract_number in ledger._accounts:
                raise ValueError(f"В файле повторяется договор {account.contract_number}")
            ledger._accounts[account.contract_number] = account
        return ledger


def build_demo_ledger():
    """Учебные договоры для демонстрации. Это не данные реальных студентов."""
    ledger = Ledger()
    ledger.add_account(
        "Иванова Мария Сергеевна",
        "Д-2026-101",
        "Разработка программного обеспечения (Full-stack разработка)",
    )
    ledger.add_charge(
        "Д-2026-101",
        "Оплата обучения",
        90000,
        date(2026, 9, 1),
        "2026/2027, 1 семестр",
    )
    ledger.add_payment("Д-2026-101", 90000, date(2026, 8, 15), "СБП")

    ledger.add_account(
        "Петров Алексей Дмитриевич",
        "Д-2026-102",
        "Разработка программного обеспечения (Full-stack разработка)",
    )
    ledger.add_charge(
        "Д-2026-102",
        "Оплата обучения",
        90000,
        date(2026, 9, 1),
        "2026/2027, 1 семестр",
    )
    ledger.add_payment("Д-2026-102", 30000, date(2026, 8, 28), "Банковский перевод")

    ledger.add_account(
        "Смирнова Ольга Павловна",
        "Д-2026-103",
        "Математическое обеспечение и администрирование информационных систем",
    )
    ledger.add_charge(
        "Д-2026-103",
        "Оплата обучения",
        80000,
        date(2026, 9, 1),
        "2026/2027, 1 семестр",
    )
    ledger.add_charge(
        "Д-2026-103",
        "Дополнительная образовательная услуга",
        5000,
        date(2026, 12, 15),
        "2026/2027, 1 семестр",
    )
    ledger.add_payment("Д-2026-103", 80000, date(2026, 9, 3), "Банковская карта")
    return ledger
