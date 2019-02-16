import logging
from typing import Callable, Any

from flask import request
from werkzeug.datastructures import ImmutableMultiDict

from songs_app.errors import InvalidQueryParameterError

logger = logging.getLogger(__name__)


def _schema_validation(schema: Callable, request_data: ImmutableMultiDict):
    try:
        query_data = schema(**request_data.to_dict())
    except (TypeError, ValueError):
        raise InvalidQueryParameterError

    return query_data


def query_validator(schema: Callable) -> Any:
    def validator(func: Callable):
        def wrapper(cls):
            query_data = _schema_validation(schema=schema, request_data=request.args)

            result = func(cls, query_data)

            return result

        return wrapper

    return validator
