# Weather Service (Make-driven)

CLI-сервис, который получает погоду из OpenWeatherMap и демонстрирует:
- управление окружением через **Makefile** (stateless)
- проверку зависимостей (imports vs requirements)
- типизацию (mypy)
- стиль (black/isort/flake8)
- тестирование (pytest + coverage)
- композитный target `make check`

## Требования
- Python 3.9+
- GNU Make
- Git

## Быстрый старт

```bash
make run