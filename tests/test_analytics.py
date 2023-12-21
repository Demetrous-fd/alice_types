import pytest

from alice_types import Analytics, AnalyticsEvent


def test_analytics_event():
    test_valid_input = '{"name":"Test","value":{}}'
    event = AnalyticsEvent.model_validate_json(test_valid_input)
    assert event.model_dump_json() == test_valid_input
    
    with pytest.raises(ValueError):
        test_invalid_input = '{"value": {"1": {"2": {"3": {"4": {"5": {"6": {}}}}}}}, "name": "Test"}'
        AnalyticsEvent.model_validate_json(test_invalid_input)
    

def test_analytics():
    test_valid_input = '{}'
    analytics = Analytics.model_validate_json(test_valid_input)
    assert len(analytics.events) == 0
    
    test_valid_input = '{"events": []}'
    analytics = Analytics.model_validate_json(test_valid_input)
    assert len(analytics.events) == 0
    
    test_valid_input = '{"events": [{"name":"Test","value":{}}]}'
    analytics = Analytics.model_validate_json(test_valid_input)
    assert len(analytics.events) == 1
    
    with pytest.raises(ValueError):
        test_invalid_input = '{"events": [{"value": {"1": {"2": {"3": {"4": {"5": {"6": {}}}}}}}, "name": "Test"}]}'
        Analytics.model_validate_json(test_invalid_input)
    
    
