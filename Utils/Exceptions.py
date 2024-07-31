from fastapi.responses import JSONResponse


class CustomHTTPException(Exception):
    def __init__(self, status_code: int, content: dict):
        self.status_code = status_code
        self.content = content


def handle_custom_exception(exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.content,
    )
