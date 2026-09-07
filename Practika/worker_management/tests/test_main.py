import sys
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from worker import Worker
import main as worker_main


class TestMainSearch(unittest.TestCase):
    def setUp(self):
        self._original_worker_list = worker_main.worker_list

    def tearDown(self):
        worker_main.worker_list = self._original_worker_list

    def test_show_workers_with_experience(self):
        current_year = datetime.now().year
        worker_main.worker_list = [
            Worker("Иванов И.И.", "Менеджер", 100000, current_year - 6),
            Worker("Петров П.П.", "Разработчик", 80000, current_year - 2),
        ]

        buffer = StringIO()

        with patch("builtins.input", return_value="3"):
            with redirect_stdout(buffer):
                worker_main.show_workers_with_experience()

        output = buffer.getvalue()
        self.assertIn("Найдены работники с таким стажем работы", output)
        self.assertIn("Иванов И.И.", output)
        self.assertNotIn("Петров П.П.", output)

