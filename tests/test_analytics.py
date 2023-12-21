import pytest

from alice_types import Analytics, AnalyticsEvent
import dataset


@pytest.mark.parametrize(
    ["obj", "expected", "raise_handler"],
    [
        dataset.ANALYTICS_EVENT["ERROR"][0].values(),
        dataset.ANALYTICS_EVENT["ERROR"][1].values(),
        dataset.ANALYTICS_EVENT["NOT_EMPTY"][0].values(),
        dataset.ANALYTICS_EVENT["NOT_EMPTY"][1].values(),
    ]
)
def test_analytics_event(obj, expected, raise_handler):
    with raise_handler:
        event = AnalyticsEvent.model_validate_json(obj.string)
        assert event.model_dump_json().encode() == expected
    

@pytest.mark.parametrize(
    ["obj", "length", "raise_handler"],
    [
        dataset.ANALYTICS["EMPTY"][0].values(),
        dataset.ANALYTICS["EMPTY"][1].values(),
        dataset.ANALYTICS["NOT_EMPTY"][0].values(),
        dataset.ANALYTICS["NOT_EMPTY"][1].values(),
        dataset.ANALYTICS["ERROR"][0].values(),
        dataset.ANALYTICS["ERROR"][1].values(),
    ]
)
def test_analytics(obj, length, raise_handler):
    with raise_handler:
        analytics = Analytics.model_validate_json(obj.string)
        assert len(analytics.events) == length
