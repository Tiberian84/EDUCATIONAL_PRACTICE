import sys
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ledger import Ledger, StudentAccount, build_demo_ledger


class TestStudentAccount(unittest.TestCase):
    def test_rejects_empty_fields(self):
        with self.assertRaises(ValueError):
            StudentAccount("  ", "Д-1", "Full-stack")
        with self.assertRaises(ValueError):
            StudentAccount("Иванов Иван", "", "Full-stack")

    def test_debt_is_charges_minus_payments(self):
        account = StudentAccount("Иванов Иван", "Д-1", "Full-stack")
        account.add_charge("Оплата обучения", 90000, date(2026, 9, 1), "1 семестр")
        account.add_payment(30000, date(2026, 8, 20), "СБП")

        self.assertEqual(account.total_charged, 90000)
        self.assertEqual(account.total_paid, 30000)
        self.assertEqual(account.debt, 60000)

    def test_rejects_non_positive_amount_and_unknown_method(self):
        account = StudentAccount("Иванов Иван", "Д-1", "Full-stack")
        with self.assertRaises(ValueError):
            account.add_charge("Оплата обучения", 0, date(2026, 9, 1), "1 семестр")
        with self.assertRaises(ValueError):
            account.add_charge("Оплата обучения", True, date(2026, 9, 1), "1 семестр")
        with self.assertRaises(ValueError):
            account.add_payment(1000, date(2026, 8, 20), "4276 1234 5678 9012")

    def test_payments_cover_earliest_charge_first(self):
        account = StudentAccount("Иванов Иван", "Д-1", "Full-stack")
        first = account.add_charge("Оплата обучения", 100, date(2026, 1, 1), "1 семестр")
        second = account.add_charge("Дополнительная услуга", 50, date(2026, 2, 1), "1 семестр")
        account.add_payment(120, date(2026, 1, 15), "Банковский перевод")

        unpaid = account.unpaid_charges()
        self.assertEqual(unpaid, [(second, 30)])
        self.assertEqual(account.overdue(date(2026, 1, 20)), [])
        self.assertEqual(account.overdue(date(2026, 3, 1)), [(second, 30)])
        self.assertNotIn(first, [charge for charge, _remainder in unpaid])

    def test_overpayment_makes_negative_debt(self):
        account = StudentAccount("Иванов Иван", "Д-1", "Full-stack")
        account.add_charge("Оплата обучения", 1000, date(2026, 9, 1), "1 семестр")
        account.add_payment(1500, date(2026, 8, 1), "СБП")

        self.assertEqual(account.debt, -500)
        self.assertEqual(account.unpaid_charges(), [])


class TestLedger(unittest.TestCase):
    def test_duplicate_contract_is_rejected(self):
        ledger = Ledger()
        ledger.add_account("Иванов Иван", "Д-1", "Full-stack")
        with self.assertRaises(ValueError):
            ledger.add_account("Петров Пётр", "Д-1", "Full-stack")

    def test_missing_contract(self):
        ledger = Ledger()
        with self.assertRaises(ValueError):
            ledger.add_payment("Д-404", 100, date(2026, 8, 1), "СБП")

    def test_debtors_and_roundtrip(self):
        ledger = build_demo_ledger()
        debtors = {account.contract_number: account.debt for account in ledger.debtors()}

        self.assertEqual(debtors, {"Д-2026-102": 60000, "Д-2026-103": 5000})
        restored = Ledger.from_dict(ledger.to_dict())
        self.assertEqual(
            {account.contract_number: account.debt for account in restored.debtors()},
            debtors,
        )

    def test_demo_overdue_on_16_november_2026(self):
        ledger = build_demo_ledger()
        rows = ledger.overdue_rows(date(2026, 11, 16))
        overdue_contracts = {account.contract_number for account, _charge, _remainder in rows}

        self.assertEqual(overdue_contracts, {"Д-2026-102"})
        self.assertEqual(rows[0][2], 60000)


if __name__ == "__main__":
    unittest.main()
