from dataclasses import asdict, is_dataclass
from decimal import Decimal
from typing import Any


def convert_dt_to_dict(dataclass: Any) -> list | dict:
    if isinstance(dataclass, list):
        return [normalize_dict(asdict(dt)) for dt in dataclass]
    elif is_dataclass(dataclass):
        return normalize_dict(asdict(dataclass))

    raise TypeError


def normalize_decimal(value):
    if isinstance(value, Decimal):
        return f"{value:.8f}"
    return value


def normalize_dict(data: dict) -> dict:
    return {key: normalize_decimal(value) for key, value in data.items()}

