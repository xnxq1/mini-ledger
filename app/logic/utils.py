from dataclasses import asdict, is_dataclass
from typing import Any


def convert_dt_to_dict(dataclass: Any) -> list | dict:
    if isinstance(dataclass, list):
        return [asdict(dt) for dt in dataclass]
    elif is_dataclass(dataclass):
        return asdict(dataclass)

    raise TypeError

