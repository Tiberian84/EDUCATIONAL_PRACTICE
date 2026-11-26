import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ledger import build_demo_ledger
from storage import load_ledger, save_ledger


class TestStorage(unittest.TestCase):
    def test_missing_file_returns_empty_ledger(self):
        ledger = load_ledger(Path(self.id()) / "missing.json")
        self.assertEqual(ledger.accounts, [])

    def test_save_and_load(self):
        folder = Path(__file__).resolve().parent / "_tmp"
        folder.mkdir(exist_ok=True)
        path = folder / "ledger.json"
        try:
            original = build_demo_ledger()
            save_ledger(original, path)
            restored = load_ledger(path)
            self.assertEqual(len(restored.accounts), 3)
            self.assertEqual(restored.get("Д-2026-101").debt, 0)
            self.assertEqual(restored.get("Д-2026-103").total_charged, 85000)
        finally:
            if path.exists():
                path.unlink()
            if folder.exists():
                folder.rmdir()

    def test_broken_file(self):
        folder = Path(__file__).resolve().parent / "_tmp_broken"
        folder.mkdir(exist_ok=True)
        path = folder / "ledger.json"
        try:
            path.write_text("{", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_ledger(path)
        finally:
            if path.exists():
                path.unlink()
            if folder.exists():
                folder.rmdir()


if __name__ == "__main__":
    unittest.main()
