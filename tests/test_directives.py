import pytest

from alice_types.response.directives import Directives
import dataset


@pytest.mark.parametrize(
    ["value", "expected", "commands", "raise_handler"],
    [
        *[data.values() for data in dataset.DIRECTIVES["EMPTY"]],
        *[data.values() for data in dataset.DIRECTIVES["NOT_EMPTY"]],
        *[data.values() for data in dataset.DIRECTIVES["ERROR"]]
    ]
)
def test_directives(value, expected, commands, raise_handler):
    with raise_handler:
        directives = Directives.model_validate_json(value.string)
        assert directives.model_dump_json(exclude_none=True).encode() == expected

        if commands is None:
            return

        set_directives = [directive for directive in directives.__dict__.values() if directive is not None]
        set_commands = list(
            map(
                lambda command: any([isinstance(directive, command) for directive in set_directives]),
                commands
            )
        )
        assert all(set_commands)
