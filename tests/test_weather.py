from unittest.mock import MagicMock, patch

import pytest
import responses

from src.weather import API_URL, WeatherResponse, display_weather, get_weather, main


@responses.activate
def test_get_weather_success(mock_weather_response: WeatherResponse) -> None:
    responses.add(responses.GET, API_URL, json=mock_weather_response, status=200)

    result = get_weather("Moscow")

    assert result["weather"][0]["description"] == "небольшой дождь"
    assert result["main"]["temp"] == 15.5
    assert result["main"]["humidity"] == 80


@responses.activate
def test_get_weather_http_error() -> None:
    responses.add(
        responses.GET, API_URL, json={"message": "city not found"}, status=404
    )

    with pytest.raises(Exception):
        get_weather("UnknownCity123")


def test_display_weather_output(
    mock_weather_response: WeatherResponse, capsys: pytest.CaptureFixture[str]
) -> None:
    display_weather(mock_weather_response, "Moscow")
    out = capsys.readouterr().out

    assert "Погода в Moscow: небольшой дождь" in out
    assert "Температура: 15.5°C" in out
    assert "Влажность: 80%" in out


@patch("src.weather.input", return_value="London")
@patch("src.weather.get_weather")
def test_main_success(
    mock_get_weather: MagicMock,
    _mock_input: MagicMock,
    mock_weather_response: WeatherResponse,
) -> None:
    mock_get_weather.return_value = mock_weather_response

    code = main()

    assert code == 0
    mock_get_weather.assert_called_once_with("London")


@patch("src.weather.input", return_value="ErrorCity")
@patch("src.weather.get_weather")
def test_main_error(mock_get_weather: MagicMock, _mock_input: MagicMock) -> None:
    from requests.exceptions import RequestException

    mock_get_weather.side_effect = RequestException("Network error")

    code = main()

    assert code == 1
