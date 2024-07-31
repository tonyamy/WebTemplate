import functools
import traceback
from functools import wraps
from typing import Any, Callable, Union, List, Dict

from fastapi.responses import JSONResponse


def to_dict(result: Any) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    if isinstance(result, list):
        return [item.__dict__ for item in result if hasattr(item, '__dict__')]
    elif hasattr(result, '__dict__'):
        return result.__dict__
    return result


def auto_convert_to_dict(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if isinstance(result, tuple) and len(result) == 2:
            results, total_count = result
            results = to_dict(results)

            # 移除 SQLAlchemy 特殊属性
            if isinstance(results, list):
                for item in results:
                    item.pop('_sa_instance_state', None)
            elif isinstance(results, dict):
                results.pop('_sa_instance_state', None)

            return results, total_count

        else:
            result = to_dict(result)

            # 移除 SQLAlchemy 特殊属性
            if isinstance(result, list):
                for item in result:
                    item.pop('_sa_instance_state', None)
            elif isinstance(result, dict):
                result.pop('_sa_instance_state', None)

            return result

    return wrapper


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
