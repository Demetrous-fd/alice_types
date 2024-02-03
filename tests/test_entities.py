import pytest
from alice_types.request.entity import Entities

import dataset


@pytest.mark.parametrize(
    ["value", "expected", "expected_fields", "type", "raise_handler"],
    [
        *[data.values() for data in dataset.ENTITY_VALUE["NOT_EMPTY"]]
    ]
)
def test_entities_value(value, expected, expected_fields, type, raise_handler):
    with raise_handler:
        if type is dict:
            assert len(set(value.obj.keys()) & set(expected_fields)) == len(expected_fields)
            return 
        
        value = type.model_validate_json(value.string)
        assert value.model_dump_json(exclude_none=True).encode() == expected
        assert value.available() == expected_fields


@pytest.mark.parametrize(
    ["value", "expected", "type", "raise_handler"],
    [
        *[data.values() for data in dataset.ENTITY["NOT_EMPTY"]],
        *[data.values() for data in dataset.ENTITY["ERROR"]]
    ]
)
def test_entities(value, expected, type, raise_handler):
    with raise_handler:        
        value = type.model_validate_json(value.string)
        assert value.model_dump_json(exclude_none=True).encode() == expected


@pytest.mark.parametrize(
    ["data", "select", "expected"],
    [
        *[data.values() for data in dataset.ENTITY["GET"]]
    ]
)
def test_entities_get(data, select, expected):
    entities = Entities.model_validate(data)

    selected_entities = entities.get(select)
    assert selected_entities == expected
