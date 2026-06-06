"""CLI-сервис погоды (OpenWeatherMap)."""

import sys
from typing import TypedDict, cast

import requests

API_URL = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = "746c9ab9cf6b08ea270ed1a4c906841c"


class WeatherInfo(TypedDict):
    description: str


class MainInfo(TypedDict):
    temp: float
    humidity: int


class WeatherResponse(TypedDict):
    weather: list[WeatherInfo]
    main: MainInfo


def get_weather(city: str) -> WeatherResponse:
    """Получает данные о погоде."""
    response = requests.get(
        API_URL,
        params={"q": city, "appid": API_KEY, "units": "metric", "lang": "ru"},
        timeout=10,
    )
    response.raise_for_status()
    return cast(WeatherResponse, response.json())


def display_weather(data: WeatherResponse, city: str) -> None:
    """Выводит погоду в консоль."""
    print(f"Погода в {city}: {data['weather'][0]['description']}")
    print(f"Температура: {data['main']['temp']}°C")
    print(f"Влажность: {data['main']['humidity']}%")


def main() -> int:
    """Точка входа."""
    city = input("Введите населенный пункт: ").strip()
    try:
        data = get_weather(city)
        display_weather(data, city)
        return 0
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
