from typing import TypeVar

from pydantic import BaseModel
from typing_extensions import Generic

R_T = TypeVar("R_T")


class Response(BaseModel, Generic[R_T]):
    data: R_T | None
    success: bool = True
    message: str = "Operation completed successfully"

