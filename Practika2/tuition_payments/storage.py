import json
from pathlib import Path

from ledger import Ledger


def save_ledger(ledger, path):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temp_path = target.with_suffix(target.suffix + ".tmp")
    temp_path.write_text(
        json.dumps(ledger.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp_path.replace(target)


def load_ledger(path):
    target = Path(path)
    if not target.exists():
        return Ledger()
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Не удалось прочитать журнал {target}: {error}") from error
    if not isinstance(data, dict):
        raise ValueError(f"Файл {target} не похож на журнал договоров")
    return Ledger.from_dict(data)
