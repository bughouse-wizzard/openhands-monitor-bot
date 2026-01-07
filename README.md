# OpenHands Monitor Bot

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

Мониторинговый бот для отслеживания задач в платформе OpenHands с отправкой уведомлений в Telegram.

## 📋 Содержание
- [Описание проекта](#описание-проекта)
- [Установка](#установка)
- [Использование](#использование)
- [Описание API функций](#описание-api-функций)
- [Контрибьютинг](#контрибьютинг)
- [Разработка](#разработка)
- [Тестирование](#тестирование)
- [Устранение неполадок](#устранение-неполадок)
- [Развертывание в production](#развертывание-в-production)
- [Лицензия](#лицензия)

## 🚀 Описание проекта

OpenHands Monitor Bot — это система мониторинга, которая отслеживает изменения в разговорах (conversations) платформы OpenHands и отправляет уведомления в Telegram о:
- Создании новых разговоров (отображаются как "задачи" в уведомлениях)
- Изменении статуса существующих разговоров
- Завершении разговоров

**Примечание о терминологии:** В контексте OpenHands API, бот отслеживает "conversations" (разговоры), но в уведомлениях они отображаются как "tasks" (задачи) для лучшей понятности пользователям.

### Основные возможности:
- **Автоматический мониторинг**: Постоянный опрос API OpenHands для отслеживания изменений
- **Уведомления в Telegram**: Мгновенные оповещения о событиях
- **Гибкая конфигурация**: Настройка через переменные окружения
- **Docker-контейнеризация**: Готовый образ для быстрого развертывания
- **Модуль словаря**: Дополнительный модуль `map_maker.py` для работы с определениями слов

### Архитектура:
- **Основной модуль**: `bot.py` — ядро системы мониторинга
- **Модуль словаря**: `map_maker.py` — работа с определениями слов
- **Тесты**: Полное покрытие тестами модуля словаря
- **Docker**: Готовые конфигурации для контейнеризации (включает оба модуля: `bot.py` и `map_maker.py`)

## 📦 Установка

### Предварительные требования
- Python 3.11 или выше
- Docker и Docker Compose (для контейнеризации)
- Аккаунт в Telegram с созданным ботом через [@BotFather](https://t.me/botfather)

### Установка зависимостей

#### Способ 1: Установка через pip
```bash
pip install -r requirements.txt
```

#### Способ 2: Установка через Docker
```bash
docker build -t openhands-monitor .
```

### Переменные окружения

Перед запуском необходимо настроить следующие переменные окружения:

| Переменная | Описание | Обязательная | Пример значения |
|------------|----------|--------------|-----------------|
| `TELEGRAM_TOKEN` | Токен вашего Telegram бота | Да | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `CHAT_ID` | ID чата для отправки уведомлений | Да | `-1001234567890` |
| `OPENHANDS_API_URL` | URL API OpenHands | Нет (по умолчанию: `http://host.docker.internal:3000`) | `http://localhost:3000` |
| `POLL_INTERVAL` | Интервал опроса API (в секундах) | Нет (по умолчанию: `5`) | `10` |

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

### Получение Telegram Chat ID
1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Добавьте бота в нужный чат/канал
3. Отправьте любое сообщение боту
4. Получите Chat ID через API:
```bash
curl "https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates"
```

## 🚀 Использование

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
```bash
# Изменение интервала опроса на 10 секунд
export POLL_INTERVAL=10
python bot.py
```

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
      - POLL_INTERVAL=30
```

## 📚 Описание API функций

### Модуль `map_maker.py`

#### Функция `get_definitions(word: str, custom_dict: dict = None) -> list`

Основная функция модуля для получения определений слов из словаря.

**Параметры:**
- `word` (str): Слово для поиска определений. Может быть строкой любого типа, включая числа, булевы значения и None (будут преобразованы в строку).
- `custom_dict` (dict, optional): Пользовательский словарь для поиска определений. Если не указан, используется стандартный словарь `STANDARD_DICTIONARY`.

**Возвращаемое значение:**
- `list`: Список определений слова. Если слово не найдено, возвращает пустой список `[]`.

**Особенности работы:**
1. **Нормализация слова**: Функция автоматически нормализует входное слово:
   - Приводит к нижнему регистру (`lower()`)
   - Удаляет лишние пробелы в начале и конце (`strip()`)
   - Обрабатывает табуляции, переносы строк и другие пробельные символы

2. **Поиск в словаре**: Поиск выполняется в следующем порядке:
   - Если передан `custom_dict`, поиск выполняется в нем
   - Если `custom_dict` не передан или равен `None`, используется стандартный словарь
   - Если слово не найдено, возвращается пустой список

3. **Обработка типов данных**:
   - Если значение в словаре не является списком, оно оборачивается в список
   - Функция всегда возвращает копию списка определений, а не ссылку на оригинал
   - Поддерживаются различные типы значений в определениях (строки, числа, словари, списки и т.д.)

**Стандартный словарь (`STANDARD_DICTIONARY`):**
Содержит следующие слова с определениями:

| Слово | Определения |
|-------|-------------|
| `apple` | 1. "A fruit that grows on trees"<br>2. "A technology company founded by Steve Jobs" |
| `python` | 1. "A high-level programming language"<br>2. "A large constricting snake" |
| `openhands` | "A platform for AI development and collaboration" |
| `test` | 1. "A procedure intended to establish the quality, performance, or reliability of something"<br>2. "An examination of someone's knowledge or proficiency" |
| `hello` | 1. "A greeting or expression of goodwill"<br>2. "Used to attract attention" |
| `world` | 1. "The earth, together with all of its countries and peoples"<br>2. "A particular region or group of countries" |

**Примеры использования:**

```python
from map_maker import get_definitions

# Базовый пример
definitions = get_definitions("apple")
print(definitions)  # ['A fruit that grows on trees', 'A technology company founded by Steve Jobs']

# С пользовательским словарем
custom_dict = {
    "python": ["Мой любимый язык программирования"],
    "openhands": ["Платформа для разработки ИИ"]
}
definitions = get_definitions("python", custom_dict)
print(definitions)  # ['Мой любимый язык программирования']

# Слово не найдено
definitions = get_definitions("nonexistent")
print(definitions)  # []

# Регистронезависимый поиск
definitions1 = get_definitions("APPLE")
definitions2 = get_definitions("apple")
definitions3 = get_definitions("Apple")
print(definitions1 == definitions2 == definitions3)  # True

# Обработка пробелов
definitions = get_definitions("  apple  ")
print(definitions)  # ['A fruit that grows on trees', 'A technology company founded by Steve Jobs']

# Нестроковые входные данные
definitions = get_definitions(123)  # Будет преобразовано в "123"
print(definitions)  # [] (если "123" нет в словаре)

# Пустая строка
definitions = get_definitions("")
print(definitions)  # []

# None как входное значение
definitions = get_definitions(None)  # Будет преобразовано в "none"
print(definitions)  # [] (если "none" нет в словаре)
```

**Обработка ошибок и граничные случаи:**
- Функция не выбрасывает исключения при некорректных входных данных
- Все некорректные типы данных преобразуются в строки
- Пустые строки и строки только из пробелов возвращают пустой список
- Если в словаре для слова указано значение `None`, оно будет возвращено как `[None]`
- Функция возвращает копию списка, поэтому модификация результата не влияет на оригинальный словарь

**Производительность:**
- Поиск выполняется за O(1) благодаря использованию словаря Python
- Функция эффективно работает с большими словарями (тысячи записей)
- Возвращается копия списка, что обеспечивает безопасность данных

### Модуль `bot.py`

#### Основные функции:

1. **`send_telegram_message(message: str)`**
   - Отправляет сообщение в настроенный Telegram чат
   - Использует механизм повторных попыток с помощью декоратора `@retry`
   - При ошибках отправки логирует их и повторяет попытку до 3 раз

2. **`fetch_conversations()`**
   - Получает список разговоров из API OpenHands
   - Использует асинхронный HTTP-клиент `httpx`
   - Обрабатывает HTTP-ошибки и ошибки соединения

3. **`poll_and_notify()`**
   - Основной цикл опроса API OpenHands
   - Сравнивает текущее состояние разговоров с предыдущим
   - Отправляет уведомления о новых разговорах и изменениях статуса
   - Очищает устаревшие записи из кэша состояний

4. **`main()`**
   - Инициализирует и запускает бота
   - Проверяет наличие обязательных переменных окружения
   - Отправляет стартовое сообщение в Telegram
   - Запускает основной цикл опроса

**Конфигурация через переменные окружения:**
- `TELEGRAM_TOKEN`: Токен Telegram бота (обязательно)
- `CHAT_ID`: ID чата для отправки уведомлений (обязательно)
- `OPENHANDS_API_URL`: URL API OpenHands (по умолчанию: `http://host.docker.internal:3000`)
- `POLL_INTERVAL`: Интервал опроса в секундах (по умолчанию: `5`)

## 🤝 Контрибьютинг

Мы приветствуем вклад в развитие проекта! Вот как вы можете помочь:

### Процесс внесения изменений
1. **Форк репозитория**
2. **Создайте ветку для вашей функции**
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
├── Dockerfile         # Конфигурация Docker (включает bot.py и map_maker.py)
├── docker-compose.yml # Конфигурация Docker Compose
├── LICENSE           # Лицензия MIT
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

Проект включает полное тестовое покрытие модуля `map_maker.py`:

### Типы тестов:
- **Базовые тесты**: Проверка основной функциональности
- **Граничные случаи**: Обработка несуществующих слов, пустых строк
- **Unicode и специальные символы**: Корректная обработка различных кодировок
- **Пользовательские словари**: Работа с кастомными словарями
- **Обработка ошибок**: Корректная обработка некорректных входных данных

### Запуск тестового покрытия:
```bash
# Генерация отчета о покрытии
python -m pytest tests/ --cov=map_maker --cov-report=html

# Просмотр отчета
open htmlcov/index.html  # На macOS
# или
xdg-open htmlcov/index.html  # На Linux
```

## 🔧 Устранение неполадок

### Распространенные проблемы и решения

#### Проблема 1: Бот не отправляет уведомления в Telegram
**Симптомы:** Бот запускается, но уведомления не приходят в Telegram.
**Возможные причины и решения:**
1. **Неверный TELEGRAM_TOKEN**: Убедитесь, что токен корректен и бот создан через @BotFather
2. **Неверный CHAT_ID**: Проверьте, что Chat ID правильный и бот добавлен в чат/канал
3. **Бот не добавлен в чат**: Убедитесь, что бот добавлен в чат/канал и имеет права на отправку сообщений
4. **Проверка токена и Chat ID**:
   ```bash
   curl "https://api.telegram.org/bot<ВАШ_ТОКЕН>/getMe"
   curl "https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates"
   ```

#### Проблема 2: Бот не может подключиться к API OpenHands
**Симптомы:** В логах появляются ошибки подключения к API.
**Возможные причины и решения:**
1. **Неверный URL API**: Проверьте переменную окружения `OPENHANDS_API_URL`
2. **API недоступен**: Убедитесь, что сервер OpenHands запущен и доступен
3. **Проблемы с сетью**: Проверьте сетевое соединение и firewall правила
4. **Тестирование подключения**:
   ```bash
   curl ${OPENHANDS_API_URL}/api/conversations
   ```

#### Проблема 3: Бот аварийно завершает работу
**Симптомы:** Бот запускается и сразу завершается с ошибкой.
**Возможные причины и решения:**
1. **Отсутствуют обязательные переменные окружения**: Проверьте `TELEGRAM_TOKEN` и `CHAT_ID`
2. **Некорректные значения переменных**: Убедитесь, что значения переменных не содержат ошибок
3. **Проблемы с зависимостями**: Переустановите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

#### Проблема 4: Docker контейнер не запускается
**Симптомы:** Контейнер сразу останавливается после запуска.
**Возможные причины и решения:**
1. **Отсутствует файл .env**: Создайте файл `.env` с необходимыми переменными
2. **Проблемы с монтированием томов**: Проверьте пути в docker-compose.yml
3. **Просмотр логов контейнера**:
   ```bash
   docker logs openhands-monitor
   docker-compose logs
   ```

#### Проблема 5: Модуль map_maker.py не возвращает определения
**Симптомы:** Функция `get_definitions` возвращает пустой список для существующих слов.
**Возможные причины и решения:**
1. **Регистр букв**: Функция регистронезависима, но проверьте правильность написания
2. **Пробелы в строке**: Функция автоматически удаляет пробелы, но проверьте входные данные
3. **Тестирование функции**:
   ```python
   from map_maker import get_definitions
   print(get_definitions("apple"))  # Должно вернуть определения
   ```

### Логирование и отладка

#### Включение подробного логирования
```python
# Добавьте в bot.py для подробного логирования
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Просмотр логов в Docker
```bash
# Просмотр логов запущенного контейнера
docker logs -f openhands-monitor

# Просмотр логов с временными метками
docker logs --timestamps openhands-monitor

# Просмотр последних 100 строк логов
docker logs --tail 100 openhands-monitor
```

#### Тестирование компонентов по отдельности
1. **Тестирование Telegram бота**:
   ```python
   import os
   from telegram import Bot
   
   bot = Bot(token=os.environ.get("TELEGRAM_TOKEN"))
   print(bot.get_me())
   ```

2. **Тестирование API OpenHands**:
   ```bash
   curl ${OPENHANDS_API_URL}/api/conversations
   ```

3. **Тестирование модуля map_maker**:
   ```bash
   python -m pytest tests/test_map_maker.py -v
   ```

### Производительность и оптимизация

#### Настройка интервала опроса
- По умолчанию: 5 секунд
- Для снижения нагрузки на API: увеличьте `POLL_INTERVAL`
- Для более быстрого реагирования: уменьшите `POLL_INTERVAL`

```bash
# Установите интервал опроса 30 секунд
export POLL_INTERVAL=30
```

#### Очистка кэша состояний
- Бот автоматически очищает устаревшие записи из кэша
- При проблемах с памятью можно уменьшить время хранения состояний

## 🚀 Развертывание в production

### Рекомендации для production среды

1. **Использование Docker Compose**:
   ```yaml
   version: '3.8'
   services:
     openhands-monitor:
       build: .
       container_name: openhands-monitor-prod
       restart: always
       network_mode: host
       environment:
         - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
         - CHAT_ID=${CHAT_ID}
         - OPENHANDS_API_URL=${OPENHANDS_API_URL}
         - POLL_INTERVAL=30
   ```

2. **Мониторинг и алертинг**:
   - Настройте мониторинг логов контейнера
   - Добавьте health checks для бота
   - Настройте алерты при остановке бота

3. **Резервное копирование**:
   - Регулярно делайте бэкапы конфигурации
   - Храните токены и секреты в безопасном месте

4. **Обновления**:
   - Регулярно обновляйте зависимости
   - Тестируйте обновления в staging среде перед production

### Масштабирование

Для обработки большого количества разговоров:
1. Увеличьте интервал опроса (`POLL_INTERVAL`)
2. Рассмотрите использование кэширования
3. При необходимости разделите мониторинг на несколько экземпляров ботов

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

## 📞 Контакты

- **Репозиторий**: [https://github.com/bughouse-wizzard/openhands-monitor-bot](https://github.com/bughouse-wizzard/openhands-monitor-bot)
- **Issues**: [https://github.com/bughouse-wizzard/openhands-monitor-bot/issues](https://github.com/bughouse-wizzard/openhands-monitor-bot/issues)

---

*Сделано с ❤️ для сообщества OpenHands*
