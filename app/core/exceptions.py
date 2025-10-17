from starlette import status



class CustomBaseException(Exception):
    status_code: int
    message: str
    detail: str | list[str]

    def __init__(
        self,
        message: str | None = None,
        detail: str | list[str] | None = None,
    ) -> None:
        if message is not None:
            self.message = message

        if detail is not None:
            self.detail = detail

        super().__init__(self.message)


class BadRequestException(CustomBaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Bad Request"
    detail = "Bad Request"


class NotFoundException(CustomBaseException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Not Found"
    detail = "Not Found"


        