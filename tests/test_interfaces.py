import pytest

from alice_types import Interfaces

import dataset


@pytest.mark.parametrize(
    ["obj", "expected", "has", "raise_handler"],
    [
        dataset.INTERFACES["EMPTY"][0].values(),
        dataset.INTERFACES["NOT_EMPTY"][0].values(),
        dataset.INTERFACES["ERROR"][0].values(),
    ]
)
def test_interface(obj, expected, has, raise_handler):
    with raise_handler:
        interfaces = Interfaces.model_validate_json(obj.string)

        assert interfaces.available() == expected

        for interface in (*expected, *has):
            assert interfaces.has(interface), f"{interfaces=} not contain {interface}"

        assert interfaces.model_dump_json(exclude_none=True).encode() == obj.string
