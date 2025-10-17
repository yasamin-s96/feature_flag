from collections import defaultdict

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api import router
from app.core.exceptions import CustomBaseException

app = FastAPI(title="Feature Flag API")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    errors = defaultdict(list)
    for err in exc.errors():
        # Ensure loc has sufficient length
        if len(err["loc"]) > 1:
            field_name = err["loc"][1]  # Field name
            error_message = err["msg"]
            errors[field_name].append(error_message)

    content = {"message": "Input validation error", "errors": errors, "success": False}

    return JSONResponse(status_code=422, content=content)


@app.exception_handler(CustomBaseException)
async def custom_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error": {"detail": exc.detail}},
    )


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)