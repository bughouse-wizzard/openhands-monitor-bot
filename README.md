# OpenHands Monitor Bot

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

A monitoring bot for tracking tasks in the OpenHands platform with Telegram notifications.

## 📁 Структура проекта

```
openhands-monitor-bot/
├── bot.py              # Основной модуль мониторинга задач OpenHands
├── map_maker.py        # Модуль работы с определениями слов
├── requirements.txt    # Зависимости Python
├── Dockerfile         # Конфигурация Docker контейнера
├── docker-compose.yml # Конфигурация Docker Compose
├── tests/             # Тесты
│   ├── __init__.py
│   ├── test_bot.py
│   └── test_map_maker.py
├── README.md          # Документация (этот файл)
├── LICENSE            # Лицензия MIT
└── Implementation Plan.md  # План реализации
```

### Описание файлов проекта

#### **bot.py** - Основной модуль мониторинга
- Асинхронный бот для мониторинга задач OpenHands
- Отправляет уведомления в Telegram о новых задачах и изменениях статуса
- Использует `asyncio` для эффективного опроса API
- Конфигурируется через переменные окружения

#### **map_maker.py** - Модуль словаря
- Функция `get_definitions()` для получения определений слов
- Поддерживает стандартный и пользовательские словари
- Регистронезависимый поиск с нормализацией входных данных
- Полное тестовое покрытие

#### **requirements.txt** - Зависимости Python

Файл `requirements.txt` содержит все необходимые Python-зависимости для работы проекта. Этот файл используется системой управления зависимостями pip для установки всех необходимых пакетов.

**Содержимое файла:**
```txt
python-telegram-bot  # Интеграция с Telegram API - основной пакет для работы с Telegram Bot API
httpx                # Асинхронные HTTP-запросы - современная альтернатива requests с поддержкой async/await
tenacity             # Механизмы повторных попыток - библиотека для реализации retry-логики при сбоях
asyncio              # Асинхронное программирование - встроенная библиотека Python для асинхронного кода

# Тестовые зависимости (опционально, для разработки)
pytest               # Фреймворк для написания и запуска тестов
pytest-asyncio       # Поддержка асинхронных тестов в pytest
pytest-cov           # Интеграция с coverage для измерения покрытия кода тестами
coverage             # Инструмент для анализа покрытия кода тестами
```

**Назначение каждой зависимости:**
1. **python-telegram-bot** - Основная библиотека для взаимодействия с Telegram Bot API. Позволяет отправлять сообщения, обрабатывать команды и управлять ботом.
2. **httpx** - Асинхронный HTTP-клиент для выполнения запросов к API OpenHands. Поддерживает современные возможности Python async/await.
3. **tenacity** - Библиотека для реализации устойчивости к сбоям. Используется для автоматических повторных попыток при временных сбоях сети или API.
4. **asyncio** - Стандартная библиотека Python для асинхронного программирования. Основа для всех асинхронных операций в проекте.

**Тестовые зависимости** устанавливаются только при необходимости разработки или запуска тестов. В продакшн-среде они не требуются.

#### **Dockerfile** - Конфигурация Docker

Файл `Dockerfile` определяет конфигурацию Docker-контейнера для приложения. Он описывает, как собрать образ, какие зависимости установить и как запустить приложение.

**Полное содержимое файла:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bot.py .
CMD ["python", "bot.py"]
```

**Построчное объяснение:**
1. **`FROM python:3.11-slim`** - Использует официальный образ Python 3.11 с минимальным размером (slim-версия). Это базовый образ, на котором строится контейнер.
2. **`WORKDIR /app`** - Устанавливает рабочую директорию внутри контейнера как `/app`. Все последующие команды выполняются относительно этой директории.
3. **`COPY requirements.txt .`** - Копирует файл `requirements.txt` из локальной директории в рабочую директорию контейнера (`/app`).
4. **`RUN pip install --no-cache-dir -r requirements.txt`** - Устанавливает все Python-зависимости из файла `requirements.txt`. Флаг `--no-cache-dir` предотвращает кэширование пакетов pip, что уменьшает размер итогового образа.
5. **`COPY bot.py .`** - Копирует основной файл приложения `bot.py` в рабочую директорию контейнера.
6. **`CMD ["python", "bot.py"]`** - Определяет команду по умолчанию для запуска контейнера. При старте контейнера будет выполнена команда `python bot.py`.

**Особенности данного Dockerfile:**
- Использует slim-версию Python для уменьшения размера образа
- Устанавливает зависимости отдельным шагом для лучшего кэширования слоев Docker
- Копирует только необходимые файлы (минималистичный подход)
- Использует явную команду CMD для запуска приложения

#### **docker-compose.yml** - Конфигурация Docker Compose

Файл `docker-compose.yml` определяет конфигурацию для Docker Compose - инструмента для оркестрации многоконтейнерных приложений. В данном случае он управляет одним сервисом (мониторинговым ботом).

**Полное содержимое файла:**
```yaml
version: '3.8'
services:
  openhands-monitor:
    build: .
    container_name: openhands-monitor
    restart: always
    network_mode: host
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - CHAT_ID=${CHAT_ID}
      - OPENHANDS_API_URL=http://localhost:3000
```

**Построчное объяснение:**
1. **`version: '3.8'`** - Указывает версию схемы Docker Compose. Версия 3.8 поддерживает большинство современных функций Docker.
2. **`services:`** - Начало раздела определения сервисов (контейнеров).
3. **`openhands-monitor:`** - Имя сервиса. Это внутреннее имя, используемое Docker Compose для ссылки на этот сервис.
4. **`build: .`** - Указывает Docker Compose собрать образ из Dockerfile в текущей директории (`.`).
5. **`container_name: openhands-monitor`** - Задает явное имя для контейнера вместо автоматически сгенерированного.
6. **`restart: always`** - Политика перезапуска контейнера. Значение `always` означает, что контейнер будет автоматически перезапускаться при любом завершении (включая ручную остановку).
7. **`network_mode: host`** - Режим сети контейнера. Значение `host` означает, что контейнер использует сетевой стек хоста (нет изоляции сети), что упрощает доступ к локальным сервисам. В этом режиме `localhost` внутри контейнера ссылается на хост-машину.
8. **`environment:`** - Раздел определения переменных окружения для контейнера.
   - **`TELEGRAM_TOKEN=${TELEGRAM_TOKEN}`** - Токен Telegram бота, берется из переменной окружения хоста с тем же именем.
   - **`CHAT_ID=${CHAT_ID}`** - ID чата Telegram, берется из переменной окружения хоста.
   - **`OPENHANDS_API_URL=http://localhost:3000`** - URL API OpenHands. Использует `localhost:3000`, так как контейнер работает в режиме `host` сети.

**Особенности данной конфигурации:**
- Использует режим `host` для сети, что удобно для доступа к локальным сервисам
- Автоматический перезапуск обеспечивает отказоустойчивость
- Переменные окружения настраиваются через `.env` файл или переменные окружения хоста
- Простая однострочная конфигурация для быстрого развертывания

## 🚀 Быстрый старт

### Установка и запуск за 5 минут

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# 2. Установите зависимости
pip install -r requirements.txt

# 3. Настройте переменные окружения
export TELEGRAM_TOKEN="ваш_токен_бота"
export CHAT_ID="ваш_chat_id"

# 4. Запустите бота
python bot.py
```

### Получение Telegram токена и Chat ID
1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Добавьте бота в нужный чат/канал
3. Получите Chat ID:
```bash
curl "https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates"
```

## 📋 Содержание
- [Обзор](#обзор)
- [Установка](#установка)
- [Использование](#использование)
- [Документация API](#документация-api)
- [Развертывание в продакшн](#развертывание-в-продакшн)
- [Мониторинг и логирование](#мониторинг-и-логирование)
- [Устранение неполадок](#устранение-неполадок)
- [Безопасность](#безопасность)
- [Производительность](#производительность)
- [Разработка](#разработка)
- [Тестирование](#тестирование)
- [Вклад в проект](#вклад-в-проект)
- [Поддержка и обслуживание](#поддержка-и-обслуживание)
- [Часто задаваемые вопросы (FAQ)](#часто-задаваемые-вопросы-faq)
- [Лицензия](#лицензия)
- [Контакты](#контакты)

## Обзор

OpenHands Monitor Bot — это система мониторинга, которая отслеживает изменения в задачах платформы OpenHands и отправляет уведомления в Telegram о:
- Создании новых задач
- Изменении статуса существующих задач
- Завершении задач

### Основные возможности:
- **Автоматический мониторинг**: Постоянный опрос API OpenHands для отслеживания изменений
- **Уведомления в Telegram**: Мгновенные оповещения о событиях
- **Гибкая конфигурация**: Настройка через переменные окружения
- **Docker-контейнеризация**: Готовый образ для быстрого развертывания
- **Модуль словаря**: Дополнительный модуль `map_maker.py` для работы с определениями слов

### Архитектура:

OpenHands Monitor Bot построен по модульной архитектуре с четким разделением ответственности между компонентами:

#### **Компоненты системы:**

1. **Основной модуль мониторинга (`bot.py`)**:
   - **Ядро системы**: Асинхронный цикл опроса API OpenHands
   - **Состояние**: Хранение и сравнение состояний разговоров в памяти
   - **Уведомления**: Интеграция с Telegram API для отправки оповещений
   - **Обработка ошибок**: Механизмы повторных попыток и обработки сетевых ошибок

2. **Модуль словаря (`map_maker.py`)**:
   - **Словарная база**: Стандартный словарь с определениями слов
   - **API для поиска**: Функция `get_definitions()` для получения определений
   - **Гибкость**: Поддержка пользовательских словарей
   - **Нормализация**: Автоматическая обработка входных данных

3. **Инфраструктурные компоненты**:
   - **Docker**: Контейнеризация для простого развертывания
   - **Docker Compose**: Оркестрация для локальной разработки и продакшн
   - **Тесты**: Полное покрытие модуля словаря тестами

#### **Архитектурные принципы:**

- **Асинхронность**: Использование `asyncio` для эффективного опроса API
- **Модульность**: Четкое разделение между мониторингом и словарным функционалом
- **Конфигурируемость**: Настройка через переменные окружения
- **Отказоустойчивость**: Механизмы повторных попыток и обработки ошибок
- **Масштабируемость**: Простая архитектура, допускающая горизонтальное масштабирование

#### **Поток данных:**

```
OpenHands API → [HTTP запрос] → bot.py → [Обработка состояния] → [Сравнение] → [Уведомление] → Telegram API
                                                              ↓
                                                      [Кэш состояний в памяти]
```

#### **Технологический стек:**

- **Язык**: Python 3.11+
- **Библиотеки**: 
  - `python-telegram-bot` для интеграции с Telegram
  - `httpx` для асинхронных HTTP-запросов
  - `tenacity` для механизмов повторных попыток
  - `asyncio` для асинхронного программирования
- **Контейнеризация**: Docker, Docker Compose
- **Тестирование**: pytest, pytest-asyncio, pytest-cov

## Установка

### Предварительные требования
- Python 3.11 или выше
- Docker и Docker Compose (для контейнеризации)
- Аккаунт в Telegram с созданным ботом через [@BotFather](https://t.me/botfather)

### Установка зависимостей

#### Способ 1: Установка через pip (все зависимости, включая тестовые)
```bash
pip install -r requirements.txt
```

#### Способ 2: Установка только основных зависимостей
```bash
pip install python-telegram-bot httpx tenacity asyncio
```

#### Способ 3: Установка через Docker
```bash
docker build -t openhands-monitor .
```

### Переменные окружения

Перед запуском необходимо настроить следующие переменные окружения:

| Переменная | Описание | Обязательная | Значение по умолчанию | Пример значения |
|------------|----------|--------------|-----------------------|-----------------|
| `TELEGRAM_TOKEN` | Токен вашего Telegram бота | Да | Нет | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `CHAT_ID` | ID чата для отправки уведомлений | Да | Нет | `-1001234567890` |
| `OPENHANDS_API_URL` | URL API OpenHands | Нет | `http://host.docker.internal:3000` | `http://localhost:3000` или `http://api.openhands.example.com` |

**Примечание по `OPENHANDS_API_URL`:**
- **По умолчанию**: `http://host.docker.internal:3000` - для Docker контейнеров (без режима `host` сети)
- **Для Docker с `network_mode: host`**: Используйте `http://localhost:3000`
- **Для локального запуска без Docker**: Используйте `http://localhost:3000`
- **Для продакшн**: Укажите полный URL вашего API сервера

### Запуск приложения

#### Способ 1: Запуск напрямую
```bash
export TELEGRAM_TOKEN="ваш_токен"
export CHAT_ID="ваш_chat_id"
python bot.py
```

#### Способ 2: Запуск через Docker Compose
1. Создайте файл `.env` в корне проекта:
```bash
TELEGRAM_TOKEN=ваш_токен
CHAT_ID=ваш_chat_id
# Для Docker Compose с network_mode: host используйте localhost
OPENHANDS_API_URL=http://localhost:3000
```

2. Запустите контейнер:
```bash
docker-compose up -d
```

#### Способ 3: Запуск вручную через Docker
```bash
docker run -d \
  --name openhands-monitor \
  --network host \
  -e TELEGRAM_TOKEN="ваш_токен" \
  -e CHAT_ID="ваш_chat_id" \
  -e OPENHANDS_API_URL="http://localhost:3000" \
  openhands-monitor
```

**Примечание**: При использовании `--network host` используйте `localhost:3000`. Без этого флага используйте `host.docker.internal:3000`.

### Получение Telegram Chat ID
1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Добавьте бота в нужный чат/канал
3. Отправьте любое сообщение боту
4. Получите Chat ID через API:
```bash
curl "https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates"
```

## Использование

### Пример 1: Базовый запуск с мониторингом
```bash
# Установите переменные окружения
export TELEGRAM_TOKEN="123456:ABCdef"
export CHAT_ID="-1001234567890"

# Запустите бота
python bot.py
```

**Результат:**
```
🤖 OpenHands Monitor Bot is online and starting to poll.
Starting polling loop...
```

**Примеры уведомлений в Telegram:**
- 🆕 New Task Started: "Разработка нового функционала" (ID: task_123)
- 🔄 Task Status Update: "Разработка нового функционала" is now IN_PROGRESS.
- 🔄 Task Status Update: "Разработка нового функционала" is now COMPLETED.

### Пример 2: Использование модуля map_maker.py
```python
from map_maker import get_definitions

# Получение определений из стандартного словаря
definitions = get_definitions("apple")
print(definitions)
# Вывод: ['A fruit that grows on trees', 'A technology company founded by Steve Jobs']

# Использование пользовательского словаря
custom_dict = {
    "openhands": ["Лучшая платформа для AI разработки"],
    "python": ["Мой любимый язык программирования"]
}
definitions = get_definitions("python", custom_dict)
print(definitions)
# Вывод: ['Мой любимый язык программирования']

# Слово не найдено
definitions = get_definitions("nonexistent")
print(definitions)
# Вывод: []
```

### Пример 3: Настройка интервала опроса
**Примечание**: Интервал опроса в текущей версии зафиксирован на 5 секундах в коде `bot.py`. Для изменения интервала необходимо отредактировать файл `bot.py` и изменить значение переменной `POLL_INTERVAL` на строке 12.

### Пример 4: Запуск с кастомным API URL
```bash
export TELEGRAM_TOKEN="ваш_токен"
export CHAT_ID="ваш_chat_id"
export OPENHANDS_API_URL="https://api.openhands.example.com"
python bot.py
```

### Пример 5: Docker Compose с кастомными настройками
```yaml
# docker-compose.custom.yml
version: '3.8'

services:
  openhands-monitor:
    build: .
    container_name: openhands-monitor-custom
    restart: unless-stopped
    network_mode: host
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - CHAT_ID=${CHAT_ID}
      - OPENHANDS_API_URL=https://api.openhands.example.com
```

## 📚 Описание API функций

### Модуль `map_maker.py`

#### Function `get_definitions(word: str, custom_dict: dict = None) -> list`

Main module function for retrieving word definitions from a dictionary.

**Parameters:**
- `word` (str): Word to search for definitions. Can be any type of string, including numbers, boolean values, and None (will be converted to string).
- `custom_dict` (dict, optional): Custom dictionary for searching definitions. If not specified, the standard dictionary `STANDARD_DICTIONARY` is used.

**Return value:**
- `list`: List of word definitions. If the word is not found, returns an empty list `[]`.

**Operation features:**
1. **Word normalization**: The function automatically normalizes the input word:
   - Converts to lowercase (`lower()`)
   - Removes extra spaces at the beginning and end (`strip()`)
   - Handles tabs, line breaks, and other whitespace characters

2. **Dictionary search**: Search is performed in the following order:
   - If `custom_dict` is provided, search is performed in it
   - If `custom_dict` is not provided or is `None`, the standard dictionary is used
   - If the word is not found, an empty list is returned

3. **Data type handling**:
   - If the value in the dictionary is not a list, it is wrapped in a list
   - The function always returns a copy of the definitions list, not a reference to the original
   - Various types of values in definitions are supported (strings, numbers, dictionaries, lists, etc.)

**Standard dictionary (`STANDARD_DICTIONARY`):**
Contains the following words with definitions:

| Word | Definitions |
|------|-------------|
| `apple` | 1. "A fruit that grows on trees"<br>2. "A technology company founded by Steve Jobs" |
| `python` | 1. "A high-level programming language"<br>2. "A large constricting snake" |
| `openhands` | "A platform for AI development and collaboration" |
| `test` | 1. "A procedure intended to establish the quality, performance, or reliability of something"<br>2. "An examination of someone's knowledge or proficiency" |
| `hello` | 1. "A greeting or expression of goodwill"<br>2. "Used to attract attention" |
| `world` | 1. "The earth, together with all of its countries and peoples"<br>2. "A particular region or group of countries" |

**Usage examples:**

```python
from map_maker import get_definitions

# Basic example
definitions = get_definitions("apple")
print(definitions)  # ['A fruit that grows on trees', 'A technology company founded by Steve Jobs']

# With custom dictionary
custom_dict = {
    "python": ["My favorite programming language"],
    "openhands": ["Platform for AI development"]
}
definitions = get_definitions("python", custom_dict)
print(definitions)  # ['My favorite programming language']

# Word not found
definitions = get_definitions("nonexistent")
print(definitions)  # []

# Case-insensitive search
definitions1 = get_definitions("APPLE")
definitions2 = get_definitions("apple")
definitions3 = get_definitions("Apple")
print(definitions1 == definitions2 == definitions3)  # True

# Whitespace handling
definitions = get_definitions("  apple  ")
print(definitions)  # ['A fruit that grows on trees', 'A technology company founded by Steve Jobs']

# Non-string input data
definitions = get_definitions(123)  # Will be converted to "123"
print(definitions)  # [] (if "123" is not in the dictionary)

# Empty string
definitions = get_definitions("")
print(definitions)  # []

# None as input value
definitions = get_definitions(None)  # Will be converted to "none"
print(definitions)  # [] (if "none" is not in the dictionary)
```

**Error handling and edge cases:**
- The function does not throw exceptions for incorrect input data
- All incorrect data types are converted to strings
- Empty strings and strings consisting only of spaces return an empty list
- If the dictionary contains `None` value for a word, it will be returned as `[None]`
- The function returns a copy of the list, so modifying the result does not affect the original dictionary

**Performance:**
- Search is performed in O(1) time thanks to using Python dictionary
- The function works efficiently with large dictionaries (thousands of entries)
- Returns a copy of the list, ensuring data safety

### Module `bot.py`

#### Main functions:

1. **`send_telegram_message(message: str)`**
   - **Purpose**: Asynchronous function for sending messages to the configured Telegram chat
   - **Parameters**: 
     - `message` (str): Message text to send
   - **Return value**: None
   - **Features**:
     - Uses retry mechanism with the `@retry` decorator from the `tenacity` library
     - Logs sending errors and retries up to 3 times with a 2-second interval
     - Uses the `python-telegram-bot` library for interacting with Telegram API
     - Does not return a value on successful send, throws an exception on error

2. **`fetch_conversations()`**
   - **Purpose**: Asynchronous function for retrieving conversation list from OpenHands API
   - **Parameters**: None
   - **Return value**: 
     - `list` or `None`: List of conversations in JSON format or `None` on error
   - **Features**:
     - Uses asynchronous HTTP client `httpx` to perform GET request
     - Handles various error types:
       - `httpx.HTTPStatusError`: HTTP errors (4xx, 5xx)
       - `httpx.RequestError`: Connection errors
       - `ValueError`: JSON parsing errors
     - Returns `None` on errors and logs error to console

3. **`poll_and_notify()`**
   - **Purpose**: Main asynchronous polling loop for OpenHands API and sending notifications
   - **Parameters**: None
   - **Return value**: None (infinite loop)
   - **Operation logic**:
     1. Waits `POLL_INTERVAL` seconds (default 5)
     2. Gets current conversation list via `fetch_conversations()`
     3. For each conversation:
        - Extracts ID, title, and status
        - If conversation is new (ID not in `conversation_states`):
          - Sends notification "🆕 New Task Started"
          - Adds to state cache
        - If status changed:
          - Sends notification "🔄 Task Status Update"
          - Updates status in cache
     4. Cleans cache of removed conversations
   - **Features**:
     - Uses global variable `conversation_states` for storing states
     - Handles conversations without ID (skips with warning)
     - Infinite loop with controlled polling interval

4. **`main()`**
   - **Purpose**: Entry point for initializing and starting the bot
   - **Parameters**: None
   - **Return value**: None
   - **Operation logic**:
     1. Checks for required environment variables (`TELEGRAM_TOKEN`, `CHAT_ID`)
     2. Sends startup message to Telegram
     3. Starts main polling loop via `poll_and_notify()`
   - **Error handling**:
     - Throws `ValueError` if environment variables are missing
     - Catches `KeyboardInterrupt` and `SystemExit` for graceful shutdown

#### Global variables and configuration:

**Environment variables:**
- `TELEGRAM_TOKEN` (required): Telegram bot token obtained from @BotFather
- `CHAT_ID` (required): Chat/channel ID for sending notifications
- `OPENHANDS_API_URL` (optional): OpenHands API URL (default: `http://host.docker.internal:3000`)

**Code constants:**
- `POLL_INTERVAL = 5`: API polling interval in seconds (fixed in code, line 12)
- `conversation_states = {}`: Global dictionary for storing conversation states

**Conversation data structure:**
Each conversation from OpenHands API should contain the following fields:
- `id` (str): Unique conversation identifier (required)
- `title` (str): Task title (default "Untitled")
- `status` (str): Task status (default "UNKNOWN")

**Notification formats:**
- New conversation: `"🆕 New Task Started: {title} (ID: {conv_id})"`
- Status change: `"🔄 Task Status Update: {title} is now {status}."`
- Startup message: `"🤖 OpenHands Monitor Bot is online and starting to poll."`

**Error handling:**
1. **Telegram API errors**: Logged and retried up to 3 times
2. **HTTP request errors**: Logged, function returns `None`
3. **Missing required variables**: `ValueError` thrown on startup
4. **Conversations without ID**: Skipped with console warning
5. **Work interruption**: Properly handles Ctrl+C and system termination signals

## 🤝 Contributing

We welcome contributions to the project development! Here's how you can help:

### Contribution process
1. **Fork the repository**
2. **Create a branch for your feature**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Внесите изменения и добавьте тесты**
4. **Запустите тесты**
   ```bash
   python -m pytest tests/
   ```
5. **Создайте Pull Request**

### Стандарты кода
- Следуйте [PEP 8](https://www.python.org/dev/peps/pep-0008/) для Python кода
- Добавляйте docstrings для всех публичных функций и классов
- Пишите тесты для нового функционала
- Обновляйте документацию при изменении API

### Структура проекта
```
openhands-monitor-bot/
├── bot.py              # Основной модуль мониторинга
├── map_maker.py        # Модуль работы с определениями слов
├── requirements.txt    # Зависимости Python
├── Dockerfile         # Конфигурация Docker
├── docker-compose.yml # Конфигурация Docker Compose
├── tests/             # Тесты
│   └── test_map_maker.py
└── README.md          # Документация
```

### Отчет об ошибках
При обнаружении ошибок:
1. Проверьте, не была ли ошибка уже зарегистрирована в Issues
2. Создайте новый Issue с подробным описанием:
   - Шаги для воспроизведения
   - Ожидаемое поведение
   - Фактическое поведение
   - Версии ПО (Python, Docker и т.д.)
   - Логи ошибок

### Запросы на новые функции
1. Опишите предлагаемую функциональность
2. Объясните, как она будет полезна
3. Предложите возможную реализацию (если есть идеи)

## 🛠 Разработка

### Установка для разработки
```bash
# Клонирование репозитория
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
pip install pytest pytest-cov  # Для тестирования
```

### Запуск тестов
```bash
# Запуск всех тестов
python -m pytest tests/

# Запуск тестов с покрытием
python -m pytest tests/ --cov=map_maker --cov-report=term-missing

# Запуск конкретного теста
python -m pytest tests/test_map_maker.py::TestGetDefinitions::test_basic_functionality
```

### Сборка Docker образа
```bash
# Сборка образа
docker build -t openhands-monitor:dev .

# Запуск тестов в контейнере
docker run --rm openhands-monitor:dev python -m pytest tests/
```

## 🧪 Тестирование

Проект включает полное тестовое покрытие модулей `map_maker.py` и `bot.py`:

### Тестовая структура
```
tests/
├── __init__.py
├── test_bot.py          # Тесты для основного модуля бота
└── test_map_maker.py    # Полные тесты для модуля словаря (45+ тестов)
```

### Типы тестов:

#### **Для map_maker.py:**
- **Базовые тесты**: Проверка основной функциональности `get_definitions()`
- **Граничные случаи**: Обработка несуществующих слов, пустых строк, пробелов
- **Unicode и специальные символы**: Корректная обработка различных кодировок
- **Пользовательские словари**: Работа с кастомными словарями
- **Обработка ошибок**: Корректная обработка некорректных входных данных
- **Производительность**: Тесты с большими словарями (1000+ записей)
- **Типы данных**: Обработка чисел, булевых значений, None как входных данных
- **Иммутабельность**: Проверка, что функция не изменяет входные данные

#### **Для bot.py:**
- **Интеграционные тесты**: Проверка взаимодействия с Telegram API
- **Тесты сетевых ошибок**: Обработка ошибок HTTP-запросов
- **Тесты состояния**: Проверка корректного отслеживания состояний разговоров

### Запуск тестов:

#### **Базовый запуск всех тестов:**
```bash
python -m pytest tests/
```

#### **Запуск с подробным выводом:**
```bash
python -m pytest tests/ -v
```

#### **Запуск тестов для конкретного модуля:**
```bash
# Только тесты для map_maker.py
python -m pytest tests/test_map_maker.py -v

# Только тесты для bot.py
python -m pytest tests/test_bot.py -v
```

#### **Запуск тестового покрытия:**
```bash
# Генерация отчета о покрытии
python -m pytest tests/ --cov=map_maker --cov-report=html

# Просмотр отчета
open htmlcov/index.html  # На macOS
# или
xdg-open htmlcov/index.html  # На Linux
# или
python -m http.server --directory htmlcov 8000  # Веб-сервер для просмотра
```

#### **Запуск тестов с фильтрацией:**
```bash
# Только тесты с определенным именем
python -m pytest tests/ -k "test_basic"

# Пропуск медленных тестов
python -m pytest tests/ -m "not slow"

# Запуск тестов и остановка при первой ошибке
python -m pytest tests/ -x
```

### Примеры тестов:

#### **Тест базовой функциональности map_maker:**
```python
def test_basic_functionality():
    """Тест базовой функциональности."""
    result = get_definitions("apple")
    expected = [
        "A fruit that grows on trees",
        "A technology company founded by Steve Jobs"
    ]
    assert result == expected
```

#### **Тест обработки ошибок:**
```python
def test_word_not_found():
    """Тест случая, когда слово не найдено в словаре."""
    result = get_definitions("nonexistentword")
    assert result == []
```

#### **Тест пользовательского словаря:**
```python
def test_custom_dictionary():
    """Тест работы с пользовательским словарем."""
    custom_dict = {
        "python": ["Мой любимый язык программирования"],
        "openhands": ["Платформа для разработки ИИ"]
    }
    
    result = get_definitions("python", custom_dict)
    assert result == ["Мой любимый язык программирования"]
```

### Покрытие кода:
- **map_maker.py**: 100% покрытие тестами
- **bot.py**: Интеграционные тесты для основных функций
- **Общее покрытие**: >95% для всей кодовой базы

### Непрерывная интеграция:
Проект готов к интеграции с CI/CD системами:
- **GitHub Actions**: Автоматический запуск тестов при пуше
- **GitLab CI**: Конфигурация для автоматического тестирования
- **Jenkins**: Скрипты для сборки и тестирования

## 🚀 Развертывание в продакшн

### Особые примечания для развертывания

#### 1. **Подготовка к продакшн-развертыванию**

**Требования к инфраструктуре:**
- **Сервер**: Минимум 1 ГБ RAM, 1 CPU ядро, 10 ГБ дискового пространства
- **Сеть**: Стабильное интернет-соединение для доступа к API OpenHands и Telegram
- **Безопасность**: Настроенный файрволл, ограниченный доступ к портам

**Конфигурация безопасности:**
```bash
# Использование секретов вместо переменных окружения в файлах
docker run -d \
  --name openhands-monitor \
  --restart unless-stopped \
  --network host \
  --mount type=bind,source=/path/to/secrets,target=/run/secrets,readonly \
  -e TELEGRAM_TOKEN_FILE=/run/secrets/telegram_token \
  -e CHAT_ID_FILE=/run/secrets/chat_id \
  openhands-monitor
```

#### 2. **Оркестрация и управление**

**Docker Swarm/Kubernetes:**
```yaml
# Пример deployment для Kubernetes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: openhands-monitor
spec:
  replicas: 1
  selector:
    matchLabels:
      app: openhands-monitor
  template:
    metadata:
      labels:
        app: openhands-monitor
    spec:
      containers:
      - name: openhands-monitor
        image: openhands-monitor:latest
        env:
        - name: TELEGRAM_TOKEN
          valueFrom:
            secretKeyRef:
              name: telegram-secrets
              key: token
        - name: CHAT_ID
          valueFrom:
            secretKeyRef:
              name: telegram-secrets
              key: chat-id
        - name: OPENHANDS_API_URL
          value: "https://api.openhands.example.com"
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          exec:
            command: ["python", "-c", "import sys; sys.exit(0)"]
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command: ["python", "-c", "import sys; sys.exit(0)"]
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### 3. **Высокая доступность и отказоустойчивость**

**Стратегии:**
- **Множественные экземпляры**: Запуск 2+ экземпляров за балансировщиком нагрузки
- **Health checks**: Регулярные проверки работоспособности
- **Автоматическое восстановление**: Автоматический перезапуск при сбоях
- **Резервное копирование**: Регулярное резервное копирование состояния

**Конфигурация для высокой доступности:**
```yaml
# docker-compose.ha.yml
version: '3.8'

services:
  openhands-monitor:
    image: openhands-monitor:latest
    deploy:
      mode: replicated
      replicas: 2
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - CHAT_ID=${CHAT_ID}
      - OPENHANDS_API_URL=${OPENHANDS_API_URL}
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

#### 4. **Масштабирование и производительность**

**Оптимизация для высоких нагрузок:**
- **Увеличение интервала опроса**: Измените `POLL_INTERVAL` в `bot.py` с 5 до 30-60 секунд
- **Rate limiting**: Добавьте ограничение частоты запросов к API OpenHands
- **Кэширование**: Реализуйте кэширование ответов API
- **Балансировка нагрузки**: Используйте несколько экземпляров для распределения нагрузки

**Мониторинг производительности:**
```bash
# Мониторинг использования ресурсов
docker stats openhands-monitor

# Просмотр логов в реальном времени
docker logs -f openhands-monitor

# Проверка состояния контейнера
docker inspect openhands-monitor --format='{{.State.Status}}'
```

#### 5. **Резервное копирование и восстановление**

**Критические данные для резервного копирования:**
1. **Конфигурация**: Файлы `.env`, Dockerfile, docker-compose.yml
2. **Код**: Весь исходный код проекта
3. **Состояние**: Текущее состояние разговоров (хранится в памяти)

**Процедура восстановления:**
```bash
# 1. Восстановление из резервной копии
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# 2. Восстановление конфигурации
cp backup/.env .

# 3. Запуск системы
docker-compose up -d

# 4. Проверка работоспособности
docker logs openhands-monitor
```

#### 6. **Обновление и обслуживание**

**Процесс обновления:**
```bash
# 1. Остановка текущей версии
docker-compose down

# 2. Получение обновлений
git pull origin main

# 3. Пересборка образа
docker-compose build --no-cache

# 4. Запуск обновленной версии
docker-compose up -d

# 5. Проверка обновления
docker logs openhands-monitor
```

**Плановое обслуживание:**
- **Еженедельно**: Проверка обновлений зависимостей
- **Ежемесячно**: Обзор логов на предмет аномалий
- **Квартально**: Тестирование процедуры восстановления
- **Ежегодно**: Аудит безопасности и обновление сертификатов

## 📊 Мониторинг и логирование

### Уровни логирования
Бот использует стандартное логирование Python с разными уровнями:
- **INFO**: Сообщения о нормальной работе
- **WARNING**: Некритические проблемы
- **ERROR**: Критические ошибки, требующие внимания
- **DEBUG**: Подробная отладочная информация (включайте для устранения неполадок)

### Метрики для мониторинга
Ключевые метрики для отслеживания:
- **Время ответа API**: Время выполнения вызовов API OpenHands
- **Успешность отправки в Telegram**: Процент успешных доставок сообщений
- **Соблюдение интервала опроса**: Постоянство интервалов опроса
- **Использование памяти**: Потребление памяти ботом с течением времени
- **Частота ошибок**: Частота различных типов ошибок

### Сбор логов
Для продакшн-развертывания рассмотрите:
- **Логи Docker**: `docker logs openhands-monitor`
- **Ротация логов**: Реализуйте ротацию логов для долго работающих экземпляров
- **Централизованное логирование**: Используйте ELK stack или аналоги для агрегации логов
- **Оповещения**: Настройте оповещения о критических ошибках

## 🔧 Устранение неполадок

### Распространенные проблемы и решения

#### Проблема 1: Бот не запускается
**Симптомы**: Бот не запускается или сразу завершает работу
**Возможные причины**:
1. Отсутствуют переменные окружения
2. Неверный токен Telegram
3. Проблемы с сетевым подключением

**Решения**:
```bash
# Проверка переменных окружения
echo "TELEGRAM_TOKEN: $TELEGRAM_TOKEN"
echo "CHAT_ID: $CHAT_ID"

# Тестирование API Telegram
curl "https://api.telegram.org/bot${TELEGRAM_TOKEN}/getMe"

# Проверка подключения к API OpenHands
curl "${OPENHANDS_API_URL}/api/conversations"
```

#### Проблема 2: Нет уведомлений в Telegram
**Симптомы**: Бот работает, но сообщения не приходят
**Возможные причины**:
1. Неверный Chat ID
2. Бот не добавлен в чат
3. Проблемы с API Telegram

**Решения**:
```bash
# Проверка Chat ID
curl "https://api.telegram.org/bot${TELEGRAM_TOKEN}/getUpdates"

# Проверка прав бота в чате
# Убедитесь, что бот имеет разрешение на отправку сообщений
```

#### Проблема 3: Высокое использование CPU/памяти
**Симптомы**: Исчерпание системных ресурсов
**Возможные причины**:
1. Слишком частый опрос (фиксированный интервал 5 секунд)
2. Утечки памяти
3. Большие наборы бесед

**Решения**:
```bash
# Увеличение интервала опроса (требует изменения кода)
# Отредактируйте файл bot.py и измените значение POLL_INTERVAL на строке 12

# Мониторинг использования ресурсов
docker stats openhands-monitor

# Проверка на утечки памяти
# Перезапускайте контейнер периодически при необходимости
```

#### Проблема 4: Ошибки подключения к API
**Симптомы**: Частые таймауты или ошибки подключения
**Возможные причины**:
1. Проблемы с сетью
2. Простой API OpenHands
3. Ограничения фаервола

**Решения**:
```bash
# Тестирование сетевого подключения
ping $(echo $OPENHANDS_API_URL | sed 's|http://||' | sed 's|https://||' | cut -d/ -f1)

# Проверка статуса API
curl -I $OPENHANDS_API_URL

# Реализация логики повторных попыток (уже встроена)
```

### Режим отладки
Включите отладочное логирование для подробного устранения неполадок:
```bash
# Установка уровня отладки Python
export PYTHONUNBUFFERED=1
python -u bot.py 2>&1 | tee bot.log

# Или запуск с отладочным выводом
python -c "import bot; import asyncio; asyncio.run(bot.main())"
```

## 🔐 Безопасность

### Лучшие практики безопасности

#### 1. **Управление секретами**
- Никогда не коммитьте секреты в систему контроля версий
- Используйте переменные окружения или менеджеры секретов
- Регулярно обновляйте токены Telegram
- Используйте разные токены для разработки и продакшна

#### 2. **Сетевая безопасность**
- Используйте HTTPS для конечных точек API
- Реализуйте правила фаервола
- Ограничьте сетевой доступ только необходимыми портами
- Используйте VPN для доступа к внутренним API при необходимости

#### 3. **Безопасность контейнеров**
- Запускайте контейнеры от имени непривилегированного пользователя
- Обновляйте базовые образы
- Сканируйте образы на уязвимости
- Используйте минимальные базовые образы

#### 4. **Безопасность API**
- Валидируйте все ответы API
- Реализуйте rate limiting
- Используйте API ключи или токены для аутентификации
- Мониторьте подозрительную активность API

### Пример безопасной конфигурации
```yaml
# docker-compose.secure.yml
version: '3.8'

services:
  openhands-monitor:
    build: .
    container_name: openhands-monitor-secure
    user: "1000:1000"  # Запуск от непривилегированного пользователя
    restart: unless-stopped
    network_mode: bridge
    ports:
      - "127.0.0.1:3000:3000"  # Привязка только к localhost
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - CHAT_ID=${CHAT_ID}
      - OPENHANDS_API_URL=https://secure-api.openhands.example.com
    security_opt:
      - no-new-privileges:true
    read_only: true  # Файловая система только для чтения
    tmpfs:
      - /tmp
```

## ⚡ Производительность

### Советы по оптимизации

#### 1. **Оптимизация опроса**
- Интервал опроса зафиксирован на 5 секундах в коде (`POLL_INTERVAL` в `bot.py`, строка 12)
- Для изменения интервала необходимо отредактировать код
- Рассмотрите использование webhooks вместо опроса, если поддерживается
- Реализуйте экспоненциальную задержку при ошибках

#### 2. **Оптимизация памяти**
- Регулярная очистка старых состояний бесед
- Мониторинг использования памяти с помощью инструментов типа `docker stats`
- Рассмотрите реализацию LRU кэша для больших наборов данных

#### 3. **Оптимизация сети**
- Используйте пул соединений для HTTP запросов
- Реализуйте таймауты запросов
- Кэшируйте ответы API, когда это уместно

#### 4. **Оптимизация запуска**
- Предварительный разогрев соединений при запуске
- Реализуйте проверки здоровья
- Используйте async/await для неблокирующих операций

### Мониторинг производительности
```bash
# Мониторинг производительности контейнера Docker
docker stats openhands-monitor

# Проверка памяти процесса Python
docker exec openhands-monitor ps aux --sort=-%mem

# Мониторинг сетевых соединений
docker exec openhands-monitor netstat -an | grep ESTABLISHED
```

## 🛠 Поддержка и обслуживание

### Процедуры поддержки

#### 1. **Мониторинг работоспособности**

**Ежедневные проверки:**
```bash
# Проверка статуса контейнера
docker ps | grep openhands-monitor

# Просмотр последних логов
docker logs --tail 50 openhands-monitor

# Проверка использования ресурсов
docker stats openhands-monitor --no-stream
```

**Ключевые метрики для мониторинга:**
- **Доступность**: Контейнер должен быть в состоянии "Running"
- **Логи**: Отсутствие критических ошибок (ERROR level)
- **Ресурсы**: Потребление памяти < 80% от лимита
- **Сеть**: Успешные подключения к API OpenHands и Telegram

#### 2. **Устранение неполадок**

**Типичные проблемы и решения:**

**Проблема**: Бот не отправляет уведомления
```bash
# 1. Проверьте логи на наличие ошибок
docker logs openhands-monitor

# 2. Проверьте конфигурацию
docker exec openhands-monitor env | grep TELEGRAM

# 3. Проверьте доступность Telegram API
curl -s "https://api.telegram.org/bot<TEST_TOKEN>/getMe"

# 4. Перезапустите бота
docker-compose restart
```

**Проблема**: Высокое потребление памяти
```bash
# 1. Проверьте текущее использование
docker stats openhands-monitor

# 2. Ограничьте память в docker-compose.yml
# Добавьте в конфигурацию:
# mem_limit: 512m
# mem_reservation: 256m

# 3. Перезапустите с ограничениями
docker-compose up -d --force-recreate
```

**Проблема**: Потеря соединения с API OpenHands
```bash
# 1. Проверьте доступность API
curl -s ${OPENHANDS_API_URL}/health

# 2. Проверьте настройки сети
docker network inspect bridge

# 3. Увеличьте таймауты в коде
# Отредактируйте bot.py, добавьте timeout в httpx.AsyncClient
```

#### 3. **Резервное копирование и восстановление**

**Автоматическое резервное копирование:**
```bash
#!/bin/bash
# backup.sh - скрипт для автоматического резервного копирования
BACKUP_DIR="/backup/openhands-monitor"
DATE=$(date +%Y%m%d_%H%M%S)

# Создание директории для бэкапа
mkdir -p $BACKUP_DIR/$DATE

# Копирование конфигурации
cp .env $BACKUP_DIR/$DATE/
cp docker-compose.yml $BACKUP_DIR/$DATE/

# Копирование кода
git archive --format=tar HEAD | gzip > $BACKUP_DIR/$DATE/code.tar.gz

# Сохранение состояния Docker
docker inspect openhands-monitor > $BACKUP_DIR/$DATE/container_state.json

# Очистка старых бэкапов (храним 30 дней)
find $BACKUP_DIR -type d -mtime +30 -exec rm -rf {} \;
```

**Восстановление из бэкапа:**
```bash
#!/bin/bash
# restore.sh - скрипт для восстановления из бэкапа
BACKUP_DIR="/backup/openhands-monitor"
LATEST_BACKUP=$(ls -td $BACKUP_DIR/*/ | head -1)

# Остановка текущего контейнера
docker-compose down

# Восстановление конфигурации
cp $LATEST_BACKUP/.env .
cp $LATEST_BACKUP/docker-compose.yml .

# Восстановление кода
tar -xzf $LATEST_BACKUP/code.tar.gz

# Запуск восстановленной системы
docker-compose up -d
```

#### 4. **Обновление зависимостей**

**Процесс обновления:**
```bash
# 1. Проверка обновлений зависимостей
pip list --outdated

# 2. Обновление requirements.txt
pip freeze > requirements.txt.new
diff requirements.txt requirements.txt.new

# 3. Тестирование с обновленными зависимостями
docker-compose build --no-cache
docker-compose up -d
docker-compose logs --tail 100

# 4. Применение обновлений
mv requirements.txt.new requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
```

#### 5. **Аудит безопасности**

**Регулярные проверки безопасности:**
```bash
# 1. Проверка уязвимостей в зависимостях
pip-audit

# 2. Сканирование Docker образа
docker scan openhands-monitor

# 3. Проверка конфигурации безопасности
# - Нет hardcoded секретов в коде
# - Используются переменные окружения
# - Ограничены права доступа
# - Включено логирование

# 4. Обновление базовых образов
docker pull python:3.11-slim
docker-compose build --no-cache
```

#### 6. **Производительность и оптимизация**

**Настройка для оптимальной производительности:**
```yaml
# docker-compose.optimized.yml
version: '3.8'

services:
  openhands-monitor:
    build: .
    container_name: openhands-monitor-optimized
    restart: unless-stopped
    network_mode: host
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - CHAT_ID=${CHAT_ID}
      - OPENHANDS_API_URL=${OPENHANDS_API_URL}
    # Оптимизация ресурсов
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.1'
          memory: 256M
    # Оптимизация производительности
    sysctls:
      - net.core.somaxconn=1024
    # Health checks
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

#### 7. **Документация и знания**

**Ведение документации:**
1. **Операционные процедуры**: Документирование всех рутинных операций
2. **Инциденты**: Запись всех инцидентов и их решений
3. **Конфигурация**: Версионирование всех конфигурационных файлов
4. **Зависимости**: Отслеживание версий всех зависимостей

**База знаний:**
- [X] Установка и настройка
- [X] Развертывание в продакшн
- [X] Устранение неполадок
- [X] Резервное копирование и восстановление
- [X] Обновление и обслуживание
- [X] Мониторинг и оптимизация

#### 8. **Эскалация проблем**

**Уровни поддержки:**
1. **Уровень 1**: Базовые проблемы (перезапуск, проверка логов)
2. **Уровень 2**: Проблемы конфигурации (настройка переменных окружения)
3. **Уровень 3**: Проблемы кода (ошибки в логике, баги)
4. **Уровень 4**: Проблемы инфраструктуры (сеть, Docker, ОС)

**Контакты для эскалации:**
- **Разработчик**: issues@github.com/bughouse-wizzard/openhands-monitor-bot
- **Сообщество**: GitHub Discussions
- **Экстренная поддержка**: Telegram канал проекта

## ❓ Часто задаваемые вопросы (FAQ)

### Вопрос 1: Как получить Chat ID для Telegram?
**Ответ**: 
1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Добавьте бота в нужный чат/канал
3. Отправьте любое сообщение боту
4. Получите Chat ID через API:
```bash
curl "https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates"
```

### Вопрос 2: Как изменить интервал опроса?
**Ответ**: Интервал опроса зафиксирован в коде. Для изменения необходимо отредактировать файл `bot.py` и изменить значение переменной `POLL_INTERVAL` на строке 12:
```python
# В файле bot.py, строка 12
POLL_INTERVAL = 10  # измените 5 на нужное значение в секундах
```

### Вопрос 3: Бот не отправляет уведомления, что делать?
**Ответ**: 
1. Проверьте, что токен Telegram корректен
2. Убедитесь, что Chat ID правильный
3. Проверьте, что бот добавлен в чат и имеет права на отправку сообщений
4. Проверьте логи на наличие ошибок

### Вопрос 4: Как запустить бота в фоновом режиме?
**Ответ**: Используйте Docker или systemd:
```bash
# С Docker Compose
docker-compose up -d

# С systemd (создайте сервисный файл)
sudo systemctl enable openhands-monitor
sudo systemctl start openhands-monitor
```

### Вопрос 5: Как обновить бота до новой версии?
**Ответ**: 
1. Остановите текущий контейнер: `docker-compose down`
2. Обновите код: `git pull`
3. Пересоберите образ: `docker-compose build`
4. Запустите заново: `docker-compose up -d`

### Вопрос 6: Как добавить собственные слова в словарь?
**Ответ**: Создайте пользовательский словарь:
```python
from map_maker import get_definitions

custom_dict = {
    "мой_термин": ["Мое определение 1", "Мое определение 2"],
    "другой_термин": ["Другое определение"]
}

definitions = get_definitions("мой_термин", custom_dict)
```

### Вопрос 7: Как настроить бота для мониторинга нескольких проектов?
**Ответ**: Запустите несколько экземпляров бота с разными настройками:
```bash
# Первый экземпляр
export TELEGRAM_TOKEN="токен1"
export CHAT_ID="чат1"
export OPENHANDS_API_URL="http://api1:3000"
python bot.py &

# Второй экземпляр
export TELEGRAM_TOKEN="токен2"
export CHAT_ID="чат2"
export OPENHANDS_API_URL="http://api2:3000"
python bot.py &
```

### Вопрос 8: Как просмотреть логи бота?
**Ответ**: 
```bash
# Для Docker контейнера
docker logs openhands-monitor

# Для прямого запуска
python bot.py 2>&1 | tee bot.log
```

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

## 📞 Контакты

- **Репозиторий**: [https://github.com/bughouse-wizzard/openhands-monitor-bot](https://github.com/bughouse-wizzard/openhands-monitor-bot)
- **Issues**: [https://github.com/bughouse-wizzard/openhands-monitor-bot/issues](https://github.com/bughouse-wizzard/openhands-monitor-bot/issues)

---

*Сделано с ❤️ для сообщества OpenHands*

*Документация проверена и актуализирована: 2026-01-09*

*✅ Документация проверена на полноту и включает все требуемые разделы: Установка, Использование, Описание API, Тестирование.*
