"""An untyped deserializer"""

import json
from typing import Any

from ..iso_8601 import iso_8601_to_timedelta, iso_8601_to_datetime
from ..config import SerializerConfig


def _deserialize_key_if_str(key: Any, config: SerializerConfig) -> Any:
    return config.deserialize_key(
        key
    ) if config.deserialize_key and isinstance(key, str) else key


def _from_value(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return iso_8601_to_datetime(value)
        except:  # pylint: disable=bare-except
            pass
        try:
            return iso_8601_to_timedelta(value)
        except:  # pylint: disable=bare-except
            pass
    return value


def _from_list(lst: list, config: SerializerConfig) -> list:
    return [
        _from_obj(item, config)
        for item in lst
    ]


def _from_dict(dct: dict, config: SerializerConfig) -> dict:
    return {
        _deserialize_key_if_str(key, config): _from_obj(value, config)
        for key, value in dct.items()
    }


def _from_obj(obj: Any, config: SerializerConfig) -> Any:
    if isinstance(obj, dict):
        return _from_dict(obj, config)
    elif isinstance(obj, list):
        return _from_list(obj, config)
    else:
        return _from_value(obj)


def deserialize(text: str, config: SerializerConfig) -> Any:
    """Deserialize JSON without type information

    Args:
        text (str): The JSON string

    Returns:
        Any: The deserialized JSON object
    """

    def _hook(obj: dict) -> dict:
        return _from_dict(obj, config)

    return json.loads(text, object_hook=_hook)
