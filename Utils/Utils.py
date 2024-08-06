import functools
import traceback
from datetime import datetime

from fastapi.responses import JSONResponse
from sqlalchemy.inspection import inspect


def to_dict(obj, formatStr='%Y-%m-%d %H:%M:%S'):
    """
    将 SQLAlchemy 对象或对象列表转换为字典，并格式化日期时间字段。
    """
    if obj is None:
        return None

    # 如果是列表，则递归调用 to_dict
    if isinstance(obj, list):
        return [to_dict(item) for item in obj]

    # 确保 obj 是 SQLAlchemy 的模型实例
    if hasattr(obj, '__table__'):
        result = {}
        mapper = inspect(obj)

        for column in mapper.mapper.column_attrs:
            value = getattr(obj, column.key)
            if isinstance(value, datetime):
                # 格式化日期时间字段
                result[column.key] = value.strftime(formatStr)
            else:
                result[column.key] = value

        return result

    # 如果不是模型实例或列表，则直接返回其自身
    return obj


def log_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            file_name, line_number, func_name, _ = tb[-1]
            print(f"Error in function '{func.__name__}': {e}")
            print(f"Function name: {func.__name__}")
            print(f"Parameters: args={args}, kwargs={kwargs}")
            print(f"Error occurred in file: {file_name}, line: {line_number}")
            raise

    return wrapper


async def custom_http_exception_handler(status_code, content):
    return JSONResponse(
        status_code=status_code,
        content=content,
    )
