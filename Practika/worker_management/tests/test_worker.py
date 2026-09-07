import sys
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from worker import Worker


class TestWorker(unittest.TestCase):
    def test_default_constructor(self):
        worker = Worker()

        self.assertEqual(worker.fio, "")
        self.assertEqual(worker.position, "")
        self.assertEqual(worker.salary, 0)
        self.assertEqual(worker.hire_year, 0)

    def test_constructor_with_values(self):
        worker = Worker("Иванов И.И.", "Менеджер", 100000, 2020)

        self.assertEqual(worker.fio, "Иванов И.И.")
        self.assertEqual(worker.position, "Менеджер")
        self.assertEqual(worker.salary, 100000)
        self.assertEqual(worker.hire_year, 2020)

    def test_factory_methods(self):
        cases = [
            (Worker.manager, ("Иванов И.И.", 2020), ("Менеджер", 100000)),
            (Worker.developer, ("Петров П.П.", 2021), ("Разработчик", 80000)),
            (Worker.designer, ("Сидоров С.С.", 2022), ("Дизайнер", 70000)),
            (Worker.analyst, ("Кузнецов А.А.", 2023), ("Аналитик", 60000)),
        ]

        for factory, args, expected in cases:
            with self.subTest(factory=factory.__name__):
                worker = factory(*args)
                self.assertEqual(worker.fio, args[0])
                self.assertEqual(worker.position, expected[0])
                self.assertEqual(worker.salary, expected[1])
                self.assertEqual(worker.hire_year, args[1])

    def test_update_changes_only_selected_fields(self):
        worker = Worker("Иванов И.И.", "Менеджер", 100000, 2020)

        worker.update(position="Аналитик")

        self.assertEqual(worker.fio, "Иванов И.И.")
        self.assertEqual(worker.position, "Аналитик")
        self.assertEqual(worker.salary, 100000)
        self.assertEqual(worker.hire_year, 2020)

    def test_update_changes_all_fields(self):
        worker = Worker("Иванов И.И.", "Менеджер", 100000, 2020)

        worker.update(
            fio="Петров П.П.",
            position="Разработчик",
            salary=85000,
            hire_year=2021,
        )

        self.assertEqual(worker.fio, "Петров П.П.")
        self.assertEqual(worker.position, "Разработчик")
        self.assertEqual(worker.salary, 85000)
        self.assertEqual(worker.hire_year, 2021)

    def test_show_prints_all_data(self):
        worker = Worker("Иванов И.И.", "Менеджер", 100000, 2020)
        buffer = StringIO()

        with redirect_stdout(buffer):
            worker.show()

        self.assertEqual(buffer.getvalue(), "Иванов И.И. Менеджер 100000 2020\n")

    def test_fio_setter_rejects_empty_value(self):
        worker = Worker()

        with self.assertRaises(ValueError):
            worker.fio = ""

    def test_salary_setter_rejects_negative_value(self):
        worker = Worker()

        with self.assertRaises(ValueError):
            worker.salary = -1

    def test_hire_year_setter_rejects_future_year(self):
        worker = Worker()
        future_year = datetime.now().year + 1

        with self.assertRaises(ValueError):
            worker.hire_year = future_year

    def test_update_uses_validation(self):
        worker = Worker("Иванов И.И.", "Менеджер", 100000, 2020)

        with self.assertRaises(ValueError):
            worker.update(salary=-100)
