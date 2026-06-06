import pytest

from src.weather import WeatherResponse


@pytest.fixture
def mock_weather_response() -> WeatherResponse:
    return {
        "weather": [{"description": "небольшой дождь"}],
        "main": {"temp": 15.5, "humidity": 80},
    }
