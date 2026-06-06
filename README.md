# Make Monorepo (FOSSDEV)

Этот репозиторий — монорепозиторий для учебных/командных проектов FOSSDEV.  
Каждый проект лежит в отдельной папке и имеет собственный README и Makefile.

## Проекты

###  weather-service
CLI-сервис для получения погоды через OpenWeatherMap, демонстрирует:
- stateless виртуальное окружение `.venv/` и запуск через `.venv/bin/...`
- проверки качества кода: lint / format / typecheck
- проверку соответствия импортов и requirements
- тестирование pytest + coverage
- единый вход через Makefile

Переход:
- Документация проекта: [weather-service/README.md](weather-service/README.md)
- Код: `weather-service/src`
- Тесты: `weather-service/tests`

## Как проверять (быстро)
```bash
cd weather-service
make check
