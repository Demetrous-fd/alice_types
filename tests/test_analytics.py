import pytest

from alice_types.response import Analytics, AnalyticsEvent
import dataset


@pytest.mark.parametrize(
    ["obj", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.ANALYTICS_EVENT["NOT_EMPTY"]],
        *[data.values() for data in dataset.ANALYTICS_EVENT["ERROR"]],
    ]
)
def test_analytics_event(obj, expected, raise_handler):
    with raise_handler:
        event = AnalyticsEvent.model_validate_json(obj.string)
        assert event.model_dump_json().encode() == expected
    

@pytest.mark.parametrize(
    ["obj", "length", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.ANALYTICS["EMPTY"]],
        *[data.values() for data in dataset.ANALYTICS["NOT_EMPTY"]],
        *[data.values() for data in dataset.ANALYTICS["ERROR"]],
    ]
)
def test_analytics(obj, length, expected, raise_handler):
    with raise_handler:
        analytics = Analytics.model_validate_json(obj.string)
        assert len(analytics.events) == length
        assert analytics.model_dump_json().encode() == expected
