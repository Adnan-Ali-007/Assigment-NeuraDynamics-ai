import os
import json
from unittest.mock import patch, Mock

from src.weather.weather_api import get_weather


def make_response(status_code=200, json_data=None):
    m = Mock()
    m.status_code = status_code
    m.json = Mock(return_value=json_data or {})
    return m


@patch("requests.get")
def test_get_weather_uses_openweather_when_key_present(mock_get, monkeypatch):
    # simulate OpenWeather response
    ow_resp = {
        "name": "TestCity",
        "weather": [{"description": "light rain"}],
        "main": {"temp": 12.34}
    }
    mock_get.return_value = make_response(200, ow_resp)

    monkeypatch.setenv("OPENWEATHER_API_KEY", "fake-key")

    res = get_weather("TestCity")
    assert "Weather in TestCity" in res
    assert "Temperature" in res


@patch("requests.get")
def test_get_weather_fallback_to_open_meteo(mock_get, monkeypatch):
    # First call is geocoding
    geo_data = {"results": [{"latitude": 12.34, "longitude": 56.78, "name": "GeoCity"}]}
    current_data = {"current_weather": {"temperature": 20.0, "weathercode": 0}}

    # Side effects: first call -> geo, second call -> forecast
    mock_get.side_effect = [make_response(200, geo_data), make_response(200, current_data)]

    # Ensure no OpenWeather key
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)

    res = get_weather("GeoCity")
    assert "Weather in GeoCity" in res or "Temperature" in res
