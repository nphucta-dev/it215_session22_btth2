from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse


def build_response(
    request: Request,
    status_code: int,
    data=None,
    message: str = "Success",
    error=None,
):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "data": data,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": str(request.url.path),
            "error": error,
        },
    )
