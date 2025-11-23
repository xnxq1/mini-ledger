from dataclasses import dataclass
from typing import Generic, TypeVar

TResult = TypeVar("TResult")
TError = TypeVar("TError")


@dataclass
class OkResponse(Generic[TResult]):
    status: int = 200
    result: TResult | None = None


@dataclass
class ErrorResponse(Generic[TError]):
    status: int = 500
    error: TError = None
