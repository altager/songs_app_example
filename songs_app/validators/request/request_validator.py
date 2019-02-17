import logging
import ujson as json
from json import JSONDecodeError
from typing import Callable, Any

from flask import request

from songs_app.errors import InvalidRequestParameterError, InvalidJSONError

logger = logging.getLogger(__name__)


def _schema_validation(schema: Callable, request_data: str):
    try:
        data = json.loads(request_data)
    except (ValueError, JSONDecodeError):
        logger.debug("Cannot load json")
        raise InvalidJSONError

    try:
        query_data = schema(**data)
    except (TypeError, ValueError):
        logger.debug(f"Request body validation error")
        raise InvalidRequestParameterError

    return query_data


def request_validator(schema: Callable) -> Any:
    def validator(func: Callable):
        def wrapper(cls):
            query_data = _schema_validation(schema=schema, request_data=request.data)

            result = func(cls, query_data)

            return result

        return wrapper

    return validator
