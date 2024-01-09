from typing import Callable
import re

from pydantic import ValidationInfo
import orjson

SPEAKER_REGEX_PATTERN = re.compile(r'<speaker audio=".*>', re.DOTALL)


def validate_tts_size(value: str, info: ValidationInfo) -> str:
    data = re.sub(SPEAKER_REGEX_PATTERN, "", value)
    data = data.encode()
    data_length = len(data)
    if data_length > 1024:
        raise ValueError(f"{info.field_name} size is big; Max bytes size: 1024; Current size: {data_length}")
    return value


def validate_dict_size(max_size: int) -> Callable:
    def validator(value: dict, info: ValidationInfo) -> dict:
        nonlocal max_size
        if isinstance(value, dict):
            data = orjson.dumps(value)
            if len(data) > max_size:
                raise ValueError(f"{info.field_name} is big; Max bytes size: {max_size}; Current size: {len(data)}")
        return value
    return validator
