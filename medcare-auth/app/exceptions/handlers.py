from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError

from app.utils.response import build_response


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return build_response(
            request,
            exc.status_code,
            data=None,
            message=exc.detail,
            error=exc.detail,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return build_response(
            request,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            data=None,
            message="Validation error",
            error=exc.errors(),
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        if isinstance(exc, HTTPException):
            raise exc
        return build_response(
            request,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=None,
            message="Internal server error",
            error=str(exc),
        )
