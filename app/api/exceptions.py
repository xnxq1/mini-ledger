from functools import partial
from typing import Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from app.api.schemas import ErrorResponse
from app.logic.balances.exceptions import BalanceAlreadyExistError, BalanceMerchantDoesNotExistError
from app.logic.merchants.exceptions import MerchantAlreadyExistError, MerchantDoesNotExistError


def register_exceptions(app: FastAPI):
    app.add_exception_handler(Exception, partial_handler(500))
    app.add_exception_handler(MerchantAlreadyExistError, partial_handler(409))
    app.add_exception_handler(BalanceAlreadyExistError, partial_handler(409))
    app.add_exception_handler(BalanceMerchantDoesNotExistError, partial_handler(404))
    app.add_exception_handler(MerchantDoesNotExistError, partial_handler(404))
    app.add_exception_handler(RequestValidationError, pydantic_handler)


def partial_handler(status_code: int) -> Callable[..., Awaitable[ORJSONResponse]]:
    return partial(exception_handler, status_code=status_code)


def exception_handler(request: Request, exc: Exception, status_code: int) -> ORJSONResponse:
    return ORJSONResponse(
        content=ErrorResponse(status=status_code, error=str(exc)),
        status_code=status_code,
    )


def pydantic_handler(request: Request, exc: RequestValidationError) -> ORJSONResponse:
    errors = exc.errors()
    errors = [error["msg"] for error in errors]
    return ORJSONResponse(
        content=ErrorResponse(status=422, error=errors),
        status_code=422,
    )
