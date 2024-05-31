# Club_Bot
Это система из нескольких ботов, которые помогают клубам по интересам вести свою деятельность.

****
## Введение в область
Основная цель клубов по интересам — объединять людей увлечённых одним направлением. Многие такие клубы имеют публичную часть для привлечения новых участников и закрытую часть для самых активных и переданных. 
Но эта “активность” никак не отслеживается админами клубов. 


## Краткое описание проекта
### Цель:
**Создать полноценную систему позволяющая клубам по интересам вести свою деятельность, а участникам чувствовать, что они часть сообщества.** 

### Описание функциональностей проекта:
- Сбор и анализ участников клуба и их активностей
- Система очков и рейтинга участников клуба
- Возможность для администратора отправлять рассылку о мероприятиях
- Возможность для администратора раздавать награды 
- Стимулирование нетворкинга и новых знакомств (random-coffee)

### Описание основных технологий, используемых в проекте:
|                                          |                            |
|------------------------------------------|----------------------------|
| Telegram бот                             | Aiogram                    |
| Бек web-приложения                       | FastAPI                    |
| Фронт web-приложения                     | html, css, js, jinja2      |
| Базы данных                              | Postgres, SQLAlchemy       |
| Подготовка, анализ и визуализация данных | Numpy, Matplotlib, Seaborn |


****
# Запуск проекта
## .env файл 
Для удобства есть пустой шаблон: [.env-template](.env-template), который нужно переименовать в .env и добавить свои переменные
## Запуск web-приложения 
```bash
## Находясь в корне проекта установка всех необходимых библиотек
pip install -r requirements.txt

# Создание новой бд
alembic init migrations
alembic revision --autogenerate -m "db creation"

# Запуск миграции
alembic upgrade head

# Запуск бека
uvicorn src.main:app --reload
```
## Запуск tg бота
```bash
## Находясь в корне проекта
cd main_bot/
python3 main.py
```

****
## Запуск tg бота для новых знакомств 
Находится в отбельной базе данных, и может работать независимо от основного бота.
```bash
## Находясь в корне проекта
cd questionnaire_bot/
python3 main.py
```

****
Если на сервере есть авто деплой, то можно использовать [docker-compose.yaml](docker-compose.yaml) и [Dockerfile](Dockerfile)
```bash
docker-compose up --build
``` 





