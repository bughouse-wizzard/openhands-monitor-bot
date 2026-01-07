# OpenHands Monitor Bot

Мониторинг задач OpenHands в реальном времени с уведомлениями в Telegram.

## 📋 Общее описание

OpenHands Monitor Bot - это система мониторинга, которая отслеживает статус задач (conversations) в OpenHands API и отправляет уведомления в Telegram о новых задачах и изменениях их статуса.

### Основные возможности:
- **Мониторинг в реальном времени**: Постоянный опрос OpenHands API для отслеживания задач
- **Уведомления в Telegram**: Мгновенные уведомления о новых задачах и изменениях статуса
- **Автоматическое обнаружение**: Автоматическое обнаружение новых и завершенных задач
- **Контейнеризация**: Готовая Docker-конфигурация для простого развертывания
- **Модуль словаря**: Дополнительный модуль для работы с определениями слов

### Архитектура проекта
Проект состоит из двух основных компонентов:
1. **Основной бот мониторинга** (`bot.py`) - отслеживает задачи OpenHands и отправляет уведомления
2. **Модуль словаря** (`map_maker.py`) - предоставляет функционал для работы с определениями слов

## 📦 Установка

### Предварительные требования
- **Python 3.11+** (для локальной установки)
- **Docker и Docker Compose** (для контейнеризованной установки)
- **Telegram Bot Token** и **Chat ID**
- **Доступ к OpenHands API** (локальный или удаленный)

### Установка через Docker (рекомендуется)

#### Шаг 1: Клонирование репозитория
```bash
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot
```

#### Шаг 2: Настройка переменных окружения
Создайте файл `.env` в корневой директории проекта:
```bash
# .env файл
TELEGRAM_TOKEN=your_telegram_bot_token_here
CHAT_ID=your_telegram_chat_id_here
OPENHANDS_API_URL=http://localhost:3000  # URL вашего OpenHands API
```

#### Шаг 3: Запуск через Docker Compose
```bash
docker-compose up -d
```

#### Шаг 4: Проверка работы
```bash
docker ps | grep openhands-monitor
docker logs openhands-monitor
```

### Установка через Python (локальная)

#### Шаг 1: Клонирование и настройка окружения
```bash
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

#### Шаг 2: Установка зависимостей
```bash
pip install -r requirements.txt
```

#### Шаг 3: Настройка переменных окружения
```bash
# Linux/macOS
export TELEGRAM_TOKEN="your_telegram_bot_token_here"
export CHAT_ID="your_telegram_chat_id_here"
export OPENHANDS_API_URL="http://localhost:3000"

# Windows (PowerShell)
$env:TELEGRAM_TOKEN="your_telegram_bot_token_here"
$env:CHAT_ID="your_telegram_chat_id_here"
$env:OPENHANDS_API_URL="http://localhost:3000"
```

#### Шаг 4: Запуск бота
```bash
python bot.py
```

## 🚀 Использование

### Запуск и работа бота

После успешной установки и настройки бот автоматически начнет мониторинг задач OpenHands. При запуске вы увидите следующие сообщения:

```
🤖 OpenHands Monitor Bot is online and starting to poll.
Starting polling loop...
```

### Типы уведомлений

Бот отправляет два типа уведомлений в Telegram:

#### 1. Новые задачи
Когда появляется новая задача в OpenHands:
```
🆕 New Task Started: Реализация фичи X (ID: 12345)
```

#### 2. Изменение статуса
Когда статус существующей задачи изменяется:
```
🔄 Task Status Update: Реализация фичи X is now COMPLETED.
```

## 📝 Описание функций

### Основной бот мониторинга (`bot.py`)

#### `send_telegram_message(message: str) -> None`
**Назначение**: Отправляет сообщение в Telegram чат с использованием токена бота.
**Особенности**:
- Использует декоратор `@retry` для 3 попыток отправки с интервалом 2 секунды
- Логирует ошибки в консоль при неудачных попытках
- Использует библиотеку `python-telegram-bot` для взаимодействия с Telegram API

#### `fetch_conversations() -> Optional[List[Dict]]`
**Назначение**: Получает список всех задач (conversations) из OpenHands API.
**Особенности**:
- Использует асинхронный HTTP-клиент `httpx` для выполнения запросов
- Обрабатывает HTTP ошибки и ошибки подключения
- Возвращает `None` при любых ошибках для безопасной обработки
- Поддерживает настраиваемый URL OpenHands API через переменную окружения

#### `poll_and_notify() -> None`
**Назначение**: Основной цикл мониторинга задач OpenHands.
**Логика работы**:
1. Ожидает `POLL_INTERVAL` секунд (по умолчанию 5)
2. Получает текущий список задач через `fetch_conversations()`
3. Сравнивает с предыдущим состоянием (`conversation_states`)
4. Отправляет уведомления об изменениях через `send_telegram_message()`
5. Очищает состояние завершенных задач

#### `main() -> None`
**Назначение**: Точка входа приложения, инициализирует и запускает бота.
**Проверки**:
- Проверяет наличие обязательных переменных окружения (`TELEGRAM_TOKEN`, `CHAT_ID`)
- Отправляет стартовое сообщение в Telegram
- Запускает основной цикл мониторинга через `poll_and_notify()`

### Модуль словаря (`map_maker.py`)

#### `get_definitions(word: str, custom_dict: dict = None) -> list`
**Назначение**: Получает определения слова из стандартного или пользовательского словаря.
**Параметры**:
- `word` (str): Слово для поиска определений
- `custom_dict` (dict, optional): Пользовательский словарь. Если не указан, используется стандартный словарь.

**Возвращает**:
- `list`: Список определений слова. Если слово не найдено, возвращает пустой список.

**Особенности**:
- Нечувствительность к регистру (приводит слово к нижнему регистру)
- Удаление лишних пробелов (использует `strip()`)
- Поддержка пользовательских словарей с приоритетом над стандартным
- Возвращает копию списка определений для предотвращения изменения оригинального словаря
- Обрабатывает различные типы входных данных (преобразует нестроковые значения в строки)

#### `STANDARD_DICTIONARY: Dict[str, List[str]]`
**Назначение**: Стандартный словарь с предопределенными словами и их значениями.
**Содержимое**: Включает определения для слов: `apple`, `python`, `openhands`, `test`, `hello`, `world` с несколькими значениями для каждого.

### Конфигурация и состояние

#### Переменные окружения
- `TELEGRAM_TOKEN`: Токен Telegram бота (обязательно)
- `CHAT_ID`: ID чата для отправки уведомлений (обязательно)
- `OPENHANDS_API_URL`: URL OpenHands API (по умолчанию: `http://host.docker.internal:3000`)
- `POLL_INTERVAL`: Интервал опроса API в секундах (по умолчанию: 5)

#### Состояние задач
Бот хранит состояние задач в памяти в словаре `conversation_states`:
- **Ключ**: ID задачи (строка)
- **Значение**: Текущий статус задачи (строка)

### Алгоритм работы системы

1. **Инициализация**: Проверка конфигурации, подключение к Telegram
2. **Цикл мониторинга**:
   - Запрос к OpenHands API для получения текущих задач
   - Сравнение с предыдущим состоянием
   - Определение изменений (новые задачи, изменение статуса)
   - Отправка соответствующих уведомлений
   - Очистка состояния завершенных задач
3. **Обработка ошибок**: Повторные попытки при сбоях сети или API
4. **Логирование**: Запись событий и ошибок в консоль



### Управление ботом

#### Запуск в фоновом режиме (Linux/macOS)
```bash
nohup python bot.py > bot.log 2>&1 &
```

#### Остановка бота
```bash
# Найти PID процесса
ps aux | grep "python bot.py"

# Остановить процесс
kill <PID>
```

#### Просмотр логов
```bash
# Docker
docker logs openhands-monitor

# Локальная установка
tail -f bot.log
```

## 🔌 Подробное описание API

### OpenHands Monitor Bot API

#### Основные функции

##### `send_telegram_message(message: str) -> None`
Отправляет сообщение в Telegram с повторными попытками при ошибках.

**Параметры:**
- `message` (str): Текст сообщения для отправки

**Особенности:**
- Использует декоратор `@retry` для 3 попыток с интервалом 2 секунды
- Логирует ошибки в консоль
- Использует библиотеку `python-telegram-bot`

##### `fetch_conversations() -> Optional[List[Dict]]`
Получает список всех задач (conversations) из OpenHands API.

**Возвращает:**
- `List[Dict]`: Список словарей с информацией о задачах
- `None`: В случае ошибки подключения

**Особенности:**
- Использует асинхронный HTTP-клиент `httpx`
- Обрабатывает HTTP ошибки и ошибки подключения
- Возвращает `None` при любых ошибках для безопасной обработки

##### `poll_and_notify() -> None`
Основной цикл мониторинга задач.

**Логика работы:**
1. Ожидает `POLL_INTERVAL` секунд (по умолчанию 5)
2. Получает текущий список задач
3. Сравнивает с предыдущим состоянием
4. Отправляет уведомления об изменениях
5. Очищает состояние завершенных задач

##### `main() -> None`
Точка входа приложения, инициализирует и запускает бота.

**Проверки:**
- Проверяет наличие обязательных переменных окружения
- Отправляет стартовое сообщение в Telegram
- Запускает основной цикл мониторинга

### Map Maker Module API

#### Константы

##### `STANDARD_DICTIONARY: Dict[str, List[str]]`
Стандартный словарь с предопределенными словами и их значениями.

**Содержимое:**
```python
{
    "apple": [
        "A fruit that grows on trees",
        "A technology company founded by Steve Jobs"
    ],
    "python": [
        "A high-level programming language", 
        "A large constricting snake"
    ],
    "openhands": [
        "A platform for AI development and collaboration"
    ],
    "test": [
        "A procedure intended to establish the quality, performance, or reliability of something",
        "An examination of someone's knowledge or proficiency"
    ],
    "hello": [
        "A greeting or expression of goodwill",
        "Used to attract attention"
    ],
    "world": [
        "The earth, together with all of its countries and peoples",
        "A particular region or group of countries"
    ]
}
```

#### Функции

##### `get_definitions(word: str, custom_dict: dict = None) -> list`
Основная функция модуля для получения определений слов.

**Параметры:**
- `word` (str): Слово для поиска определений
- `custom_dict` (dict, optional): Пользовательский словарь

**Возвращает:**
- `list`: Список определений слова
- Пустой список `[]`, если слово не найдено

**Алгоритм работы:**
1. Нормализует входное слово (нижний регистр, удаление пробелов)
2. Выбирает словарь для поиска (пользовательский или стандартный)
3. Возвращает определения или пустой список

### Внешние API интеграции

#### Telegram Bot API
- **Endpoint**: `https://api.telegram.org/bot{token}/sendMessage`
- **Метод**: POST
- **Параметры**: `chat_id`, `text`
- **Библиотека**: `python-telegram-bot`

#### OpenHands API
- **Endpoint**: `{OPENHANDS_API_URL}/api/conversations`
- **Метод**: GET
- **Ответ**: JSON массив объектов задач
- **Структура задачи**:
  ```json
  {
    "id": "string",
    "title": "string",
    "status": "string",
    "createdAt": "timestamp",
    "updatedAt": "timestamp"
  }
  ```

## 📚 Примеры

### Пример 1: Базовое использование бота мониторинга

#### Настройка и запуск
```bash
# Установка переменных окружения
export TELEGRAM_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
export CHAT_ID="-1001234567890"
export OPENHANDS_API_URL="http://localhost:3000"

# Запуск бота
python bot.py
```

#### Ожидаемый вывод
```
🤖 OpenHands Monitor Bot is online and starting to poll.
Starting polling loop...
```

#### Примеры уведомлений в Telegram
```
🆕 New Task Started: Реализация фичи X (ID: 12345)
🔄 Task Status Update: Реализация фичи X is now COMPLETED.
🆕 New Task Started: Исправление бага Y (ID: 67890)
🔄 Task Status Update: Исправление бага Y is now IN_PROGRESS.
```

### Пример 2: Использование модуля Map Maker

#### Базовое использование
```python
from map_maker import get_definitions

# Получение определений из стандартного словаря
result = get_definitions("python")
print(result)
# Output: ['A high-level programming language', 'A large constricting snake']

# Работа с различными форматами ввода
print(get_definitions("  APPLE  "))  # ['A fruit that grows on trees', 'A technology company...']
print(get_definitions("Python"))     # ['A high-level programming language', 'A large constricting snake']
print(get_definitions("HELLO"))      # ['A greeting or expression of goodwill', 'Used to attract attention']
```

#### Использование пользовательского словаря
```python
from map_maker import get_definitions

# Создание пользовательского словаря
custom_dict = {
    "docker": ["Контейнеризация приложений", "Платформа для разработки"],
    "kubernetes": ["Оркестратор контейнеров", "Система управления кластерами"],
    "openhands": ["Моя любимая платформа для разработки ИИ"]
}

# Поиск в пользовательском словаре
result = get_definitions("docker", custom_dict)
print(result)
# Output: ['Контейнеризация приложений', 'Платформа для разработки']

# Приоритет пользовательского словаря
result = get_definitions("openhands", custom_dict)
print(result)
# Output: ['Моя любимая платформа для разработки ИИ'] (вместо стандартного определения)
```

#### Обработка отсутствующих слов
```python
from map_maker import get_definitions

# Слова нет в словаре
result = get_definitions("nonexistentword")
print(result)
# Output: []

# Пустая строка
result = get_definitions("")
print(result)
# Output: []

# Только пробелы
result = get_definitions("   ")
print(result)
# Output: []
```

### Пример 3: Интеграция с другими системами

#### Использование в веб-приложении
```python
from flask import Flask, request, jsonify
from map_maker import get_definitions

app = Flask(__name__)

@app.route('/api/definitions', methods=['GET'])
def get_word_definitions():
    word = request.args.get('word', '')
    definitions = get_definitions(word)
    return jsonify({
        'word': word,
        'definitions': definitions,
        'count': len(definitions)
    })

if __name__ == '__main__':
    app.run(debug=True)
```

#### Использование в скрипте анализа текста
```python
from map_maker import get_definitions
import re

def analyze_text(text):
    """Извлекает ключевые слова и их определения из текста."""
    words = re.findall(r'\b\w+\b', text.lower())
    results = {}
    
    for word in set(words):  # Убираем дубликаты
        definitions = get_definitions(word)
        if definitions:
            results[word] = definitions
    
    return results

# Пример использования
text = "Python is a great programming language for AI development with OpenHands."
analysis = analyze_text(text)
print(analysis)
# Output: {
#     'python': ['A high-level programming language', 'A large constricting snake'],
#     'openhands': ['A platform for AI development and collaboration']
# }
```

### Пример 4: Расширение функциональности

#### Создание производного модуля
```python
# advanced_map_maker.py
from map_maker import get_definitions, STANDARD_DICTIONARY

class AdvancedDictionary:
    def __init__(self):
        self.custom_dict = {}
    
    def add_definition(self, word, definition):
        """Добавляет определение к слову."""
        word = word.strip().lower()
        if word not in self.custom_dict:
            self.custom_dict[word] = []
        self.custom_dict[word].append(definition)
    
    def get_all_definitions(self, word):
        """Получает все определения слова из всех источников."""
        # Получаем из пользовательского словаря
        custom_defs = self.custom_dict.get(word.strip().lower(), [])
        
        # Получаем из стандартного словаря
        standard_defs = get_definitions(word)
        
        # Объединяем, убирая дубликаты
        all_defs = custom_defs + [d for d in standard_defs if d not in custom_defs]
        return all_defs

# Использование
advanced_dict = AdvancedDictionary()
advanced_dict.add_definition("ai", "Artificial Intelligence")
advanced_dict.add_definition("ai", "Искусственный интеллект")

result = advanced_dict.get_all_definitions("ai")
print(result)
# Output: ['Artificial Intelligence', 'Искусственный интеллект']
```

## 🔐 Авторизация

### Аутентификация и безопасность

#### Telegram Bot Token
Для работы с Telegram API требуется токен бота, который обеспечивает:
- **Идентификацию**: Уникальный идентификатор вашего бота
- **Авторизацию**: Права на отправку сообщений от имени бота
- **Безопасность**: Защищенный доступ к Telegram API

**Получение токена:**
1. Создайте бота через @BotFather в Telegram
2. Сохраните токен в безопасном месте
3. Никогда не коммитьте токен в репозиторий

#### OpenHands API доступ
Бот взаимодействует с OpenHands API для получения информации о задачах:

**Требования к доступу:**
- **URL API**: Должен быть доступен из среды выполнения бота
- **Сетевой доступ**: Отсутствие блокировок firewall
- **CORS**: При необходимости настроить CORS политики

### Безопасное хранение учетных данных

#### Переменные окружения (рекомендуется)
Используйте переменные окружения для хранения чувствительных данных:

```bash
# .env файл (не коммитить в репозиторий!)
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
CHAT_ID=-1001234567890
```

#### Docker Secrets (для продакшена)
```bash
# Создание секретов
echo "your_telegram_token" | docker secret create telegram_token -
echo "your_chat_id" | docker secret create chat_id -

# Использование в docker-compose.yml
services:
  openhands-monitor:
    image: openhands-monitor-bot
    secrets:
      - telegram_token
      - chat_id
    environment:
      - TELEGRAM_TOKEN_FILE=/run/secrets/telegram_token
      - CHAT_ID_FILE=/run/secrets/chat_id
```

#### Kubernetes Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: bot-secrets
type: Opaque
stringData:
  telegram-token: "your_telegram_token"
  chat-id: "your_chat_id"
```

### Права доступа

#### Минимальные необходимые права
1. **Telegram Bot**:
   - Отправка сообщений в указанный чат
   - Чтение обновлений (для получения Chat ID)

2. **OpenHands API**:
   - Чтение списка задач (GET /api/conversations)
   - Доступ только для чтения

#### Рекомендации по безопасности
1. **Изоляция среды**: Запускайте бота в изолированной среде (Docker, виртуальная машина)
2. **Ограничение сетевого доступа**: Настройте firewall для ограничения входящих/исходящих соединений
3. **Регулярное обновление**: Обновляйте зависимости для устранения уязвимостей
4. **Мониторинг логов**: Регулярно проверяйте логи на предмет подозрительной активности
5. **Ротация токенов**: Периодически обновляйте Telegram Bot Token

### Аудит и логирование

#### Логи безопасности
Бот ведет логи следующих событий:
- Успешная аутентификация и запуск
- Ошибки подключения к API
- Неудачные попытки отправки сообщений
- Изменения в состоянии задач

#### Мониторинг доступа
```bash
# Просмотр логов Docker контейнера
docker logs --tail 100 openhands-monitor

# Поиск подозрительной активности
docker logs openhands-monitor | grep -i "error\|fail\|unauthorized"
```

### Инциденты безопасности

#### Действия при компрометации токена
1. **Немедленно отозвать токен** через @BotFather
2. **Создать новый токен** и обновить переменные окружения
3. **Проверить логи** на предмет несанкционированного доступа
4. **Обновить все среды** с новым токеном

#### Защита от DDoS атак
- Используйте `POLL_INTERVAL` для ограничения частоты запросов
- Реализуйте экспоненциальную задержку при ошибках
- Рассмотрите использование rate limiting на стороне API

### Совместимость и миграция

#### Миграция учетных данных
При переносе бота между средами:
1. Экспортируйте переменные окружения из старой среды
2. Импортируйте в новую среду
3. Проверьте работоспособность
4. Отзовите старые токены при необходимости

#### Версионность API
- **Telegram Bot API**: Совместимость с текущей версией библиотеки `python-telegram-bot`
- **OpenHands API**: Совместимость с текущей структурой ответа `/api/conversations`

### Дополнительные меры безопасности

#### Шифрование конфигурации
Для дополнительной безопасности можно использовать шифрование:

```python
# Пример использования шифрованных переменных окружения
import os
from cryptography.fernet import Fernet

def decrypt_value(encrypted_value):
    key = os.environ.get('ENCRYPTION_KEY')
    cipher = Fernet(key.encode())
    return cipher.decrypt(encrypted_value.encode()).decode()

TELEGRAM_TOKEN = decrypt_value(os.environ.get('ENCRYPTED_TELEGRAM_TOKEN'))
```

#### Двухфакторная аутентификация
Для критически важных систем рассмотрите:
1. Верификацию отправки уведомлений через второй канал
2. Подтверждение критических действий
3. Аудит всех операций

## 🧪 Тестирование

### Запуск тестов
```bash
python -m pytest test_map_maker.py -v
```

### Покрытие тестами
Модуль `map_maker.py` имеет 100% покрытие тестами, включая:
- Базовые случаи использования
- Обработку граничных значений
- Unicode и специальные символы
- Различные типы входных данных
- Пользовательские словари

## 🐳 Docker развертывание

### Сборка образа
```bash
docker build -t openhands-monitor-bot .
```

### Запуск контейнера
```bash
docker run -d \
  --name openhands-monitor \
  --network host \
  -e TELEGRAM_TOKEN="your_token" \
  -e CHAT_ID="your_chat_id" \
  openhands-monitor-bot
```

### Docker Compose
```bash
# Создайте .env файл с переменными окружения
echo "TELEGRAM_TOKEN=your_token" > .env
echo "CHAT_ID=your_chat_id" >> .env

# Запустите
docker-compose up -d
```

## 🔄 Логика работы

### Алгоритм мониторинга
1. **Инициализация**: Проверка конфигурации и подключение к Telegram
2. **Опрос API**: Каждые 5 секунд запрос к `/api/conversations`
3. **Анализ изменений**:
   - Новые задачи → уведомление "🆕 New Task Started"
   - Изменение статуса → уведомление "🔄 Task Status Update"
   - Завершенные задачи → удаление из состояния
4. **Обработка ошибок**: Повторные попытки при сбоях сети/API

### Состояние задач
Бот хранит состояние задач в памяти (`conversation_states` словарь):
- Ключ: ID задачи
- Значение: Текущий статус

## 🛠️ Разработка

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
```

### Зависимости
- `python-telegram-bot` - Работа с Telegram API
- `httpx` - Асинхронные HTTP-запросы
- `tenacity` - Повторные попытки при ошибках
- `asyncio` - Асинхронное программирование

### Структура кода

#### Основные функции `bot.py`:
- `send_telegram_message()` - Отправка сообщений в Telegram с повторными попытками
- `fetch_conversations()` - Получение списка задач из OpenHands API
- `poll_and_notify()` - Основной цикл мониторинга
- `main()` - Точка входа приложения

#### Основные функции `map_maker.py`:
- `get_definitions()` - Получение определений слова из словаря

## 📊 Мониторинг и логи

### Логирование
Бот выводит логи в консоль:
- Старт/остановка бота
- Ошибки подключения
- Успешные уведомления

### Проверка работоспособности
1. Проверьте, что бот запущен:
```bash
docker ps | grep openhands-monitor
```

2. Проверьте логи:
```bash
docker logs openhands-monitor
```

## 🔒 Безопасность

### Рекомендации по безопасности
1. **Хранение токенов**: Используйте переменные окружения или секреты Docker
2. **Доступ к API**: Ограничьте доступ к OpenHands API
3. **Обновления**: Регулярно обновляйте зависимости

### Переменные окружения в продакшене
Используйте секреты Docker или менеджеры секретов:
```bash
# Docker Swarm
echo "TELEGRAM_TOKEN" | docker secret create telegram_token -

# Kubernetes
kubectl create secret generic bot-secrets \
  --from-literal=TELEGRAM_TOKEN=your_token \
  --from-literal=CHAT_ID=your_chat_id
```

## 🐛 Устранение неполадок

### Распространенные проблемы

**Проблема**: Бот не отправляет уведомления
**Решение**: Проверьте:
1. Корректность TELEGRAM_TOKEN и CHAT_ID
2. Доступность OpenHands API
3. Наличие бота в чате

**Проблема**: Ошибки подключения к API
**Решение**: Убедитесь, что:
1. OPENHANDS_API_URL указан правильно
2. API доступен из контейнера
3. Нет блокировок firewall

**Проблема**: Docker контейнер не запускается
**Решение**: Проверьте:
1. Наличие .env файла
2. Права доступа к файлам
3. Состояние портов

### Логи ошибок
```bash
# Просмотр логов Docker
docker logs openhands-monitor

# Просмотр логов с деталями
docker logs --tail 50 -f openhands-monitor
```

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие OpenHands Monitor Bot! Вот как вы можете помочь:

### 🐛 Отчеты об ошибках

Если вы обнаружили ошибку, пожалуйста:

1. **Проверьте существующие issues** на GitHub, чтобы убедиться, что проблема еще не была зарегистрирована
2. **Создайте новый issue** с четким и описательным заголовком
3. **Включите следующую информацию**:
   - Краткое описание проблемы
   - Шаги для воспроизведения
   - Ожидаемое поведение
   - Фактическое поведение
   - Версии ПО (Python, Docker и т.д.)
   - Скриншоты или логи (если применимо)
   - Контекст проблемы (как она влияет на вас)

### 💡 Запросы на добавление функциональности

Есть идея для улучшения? Мы будем рады ее рассмотреть:

1. **Проверьте существующие issues** и обсуждения
2. **Создайте issue с предложением**:
   - Опишите предлагаемую функциональность
   - Объясните преимущества и варианты использования
   - Предложите возможную реализацию (если есть идеи)
   - Укажите, готовы ли вы помочь с реализацией

### 👨‍💻 Разработка

Хотите внести код? Отлично! Вот процесс:

#### 1. Настройка среды разработки
```bash
# Клонируйте репозиторий
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt
pip install -e .  # Для разработки
```

#### 2. Создание ветки для разработки
```bash
# Создайте новую ветку от main
git checkout -b feature/ваша-фича

# Или для исправления ошибки
git checkout -b fix/описание-исправления
```

#### 3. Стандарты кода
- Следуйте стилю кода проекта (PEP 8 для Python)
- Добавляйте документацию к новым функциям и классам
- Пишите чистый, читаемый код с понятными названиями переменных
- Добавляйте комментарии там, где логика не очевидна

#### 4. Тестирование
```bash
# Запустите все тесты
python -m pytest tests/ -v

# Запустите тесты с покрытием
python -m pytest tests/ --cov=map_maker --cov-report=term-missing

# Проверьте стиль кода
python -m flake8 bot.py map_maker.py tests/
```

**Требования к тестам**:
- Новый код должен включать соответствующие тесты
- Тесты должны покрывать как позитивные, так и негативные сценарии
- Стремитесь к 100% покрытию для нового кода
- Тесты должны быть независимыми и воспроизводимыми

#### 5. Документация
- Обновите README.md, если ваши изменения влияют на использование
- Добавьте документацию к новым функциям/классам
- Обновите примеры использования, если применимо
- Убедитесь, что документация остается актуальной

#### 6. Создание Pull Request
1. **Убедитесь, что все тесты проходят**
2. **Обновите документацию** при необходимости
3. **Создайте Pull Request** на GitHub:
   - Укажите ясное описание изменений
   - Ссылайтесь на соответствующий issue (если есть)
   - Опишите тестирование, которое вы провели
   - Укажите любые breaking changes

#### 7. Процесс ревью кода
- Будьте готовы к обсуждению и доработкам
- Отвечайте на комментарии ревьюверов
- Вносите необходимые изменения
- Поддерживайте конструктивный диалог

### 📋 Области для вклада

#### Приоритетные задачи:
1. **Улучшение обработки ошибок**: Более надежная обработка сетевых сбоев
2. **Расширение функциональности мониторинга**: Новые типы уведомлений, фильтрация
3. **Улучшение производительности**: Оптимизация использования памяти и CPU
4. **Дополнительные интеграции**: Поддержка других мессенджеров или систем мониторинга
5. **Улучшение документации**: Перевод на другие языки, больше примеров

#### Начинающим разработчикам:
- Исправление опечаток в документации
- Улучшение тестового покрытия
- Добавление примеров использования
- Создание issue с предложениями по улучшению

### 🏆 Признание вклада

Все значимые вклады будут отмечены в:
- Файле CONTRIBUTORS.md (если будет создан)
- Release notes
- Соответствующем разделе документации

### 📜 Кодекс поведения

Мы ожидаем, что все участники будут соблюдать [Кодекс поведения Contributor Covenant](https://www.contributor-covenant.org/). Пожалуйста, будьте уважительны и конструктивны в обсуждениях.

### ❓ Вопросы и помощь

Если у вас есть вопросы или нужна помощь:
1. Проверьте документацию и существующие issues
2. Создайте issue с вопросом
3. Присоединяйтесь к обсуждениям в существующих issues

Спасибо за ваш вклад в развитие OpenHands Monitor Bot! 🚀

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле LICENSE.

## 📞 Поддержка

- **Issues**: [GitHub Issues](https://github.com/bughouse-wizzard/openhands-monitor-bot/issues)
- **Документация**: Этот README файл
- **Примеры**: См. раздел "Использование"

---

*Последнее обновление: 2026-01-06*