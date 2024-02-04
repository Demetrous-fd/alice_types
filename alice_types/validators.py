from typing import Callable, Union
import re
import os

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


class DynamicSize:
    def __init__(self, name: str, value: int):
        self.name = f"ALICE_TYPES:{name}"
        os.environ[self.name] = str(value)

    @property
    def value(self):
        return int(os.getenv(self.name))

    @value.setter
    def value(self, value):
        os.environ[self.name] = str(value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __gt__(self, other: int):
        return self.value > other

    def __lt__(self, other: int):
        return self.value < other


def validate_dict_size(max_size: Union[int, DynamicSize]) -> Callable:
    def validator(value: dict, info: ValidationInfo) -> dict:
        nonlocal max_size
        if isinstance(value, dict):
            data = orjson.dumps(value)
            if len(data) > max_size:
                raise ValueError(f"{info.field_name} is big; Max bytes size: {max_size}; Current size: {len(data)}")
        return value
    return validator
