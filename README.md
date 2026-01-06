# OpenHands Monitor Bot

Мониторинг задач OpenHands в реальном времени с уведомлениями в Telegram.

## 📋 Обзор проекта

OpenHands Monitor Bot - это система мониторинга, которая отслеживает статус задач (conversations) в OpenHands API и отправляет уведомления в Telegram о новых задачах и изменениях их статуса.

### Основные возможности:
- **Мониторинг в реальном времени**: Постоянный опрос OpenHands API для отслеживания задач
- **Уведомления в Telegram**: Мгновенные уведомления о новых задачах и изменениях статуса
- **Автоматическое обнаружение**: Автоматическое обнаружение новых и завершенных задач
- **Контейнеризация**: Готовая Docker-конфигурация для простого развертывания
- **Модуль словаря**: Дополнительный модуль для работы с определениями слов

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.11+
- Docker и Docker Compose (опционально)
- Telegram Bot Token и Chat ID

### Установка

#### Способ 1: Установка через Docker (рекомендуется)

1. Клонируйте репозиторий:
```bash
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot
```

2. Создайте файл `.env` с вашими настройками:
```bash
TELEGRAM_TOKEN=your_telegram_bot_token_here
CHAT_ID=your_telegram_chat_id_here
```

3. Запустите через Docker Compose:
```bash
docker-compose up -d
```

#### Способ 2: Установка через Python

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Установите переменные окружения:
```bash
export TELEGRAM_TOKEN="your_telegram_bot_token_here"
export CHAT_ID="your_telegram_chat_id_here"
export OPENHANDS_API_URL="http://localhost:3000"  # URL вашего OpenHands API
```

3. Запустите бота:
```bash
python bot.py
```

## ⚙️ Конфигурация

### Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `TELEGRAM_TOKEN` | Токен вашего Telegram бота | **Обязательно** |
| `CHAT_ID` | ID чата для отправки уведомлений | **Обязательно** |
| `OPENHANDS_API_URL` | URL OpenHands API | `http://host.docker.internal:3000` |
| `POLL_INTERVAL` | Интервал опроса API (секунды) | `5` |

### Получение Telegram Bot Token
1. Откройте Telegram и найдите @BotFather
2. Создайте нового бота с помощью команды `/newbot`
3. Сохраните полученный токен

### Получение Chat ID
1. Добавьте бота в нужный чат
2. Отправьте любое сообщение боту
3. Перейдите по ссылке: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Найдите `chat.id` в ответе JSON

## 🏗️ Архитектура проекта

### Структура файлов
```
openhands-monitor-bot/
├── bot.py                    # Основной файл бота
├── map_maker.py              # Модуль для работы с определениями слов
├── test_map_maker.py         # Тесты для модуля map_maker
├── requirements.txt          # Зависимости Python
├── Dockerfile               # Конфигурация Docker
├── docker-compose.yml       # Конфигурация Docker Compose
├── README.md                # Эта документация
└── Implementation Plan.md   # План реализации
```

### Основные компоненты

#### 1. OpenHands Monitor Bot (`bot.py`)
Основной модуль бота, который:
- Опрашивает OpenHands API каждые 5 секунд
- Отслеживает изменения статуса задач
- Отправляет уведомления в Telegram
- Управляет состоянием задач в памяти

#### 2. Map Maker Module (`map_maker.py`)
Вспомогательный модуль для работы со словарями:
- **Основная функция**: `get_definitions(word, custom_dict)` - получение определений слов
- **Стандартный словарь**: Встроенный словарь с определениями общих терминов
- **Поддержка пользовательских словарей**: Возможность использования внешних словарей
- **Нормализация ввода**: Автоматическая обработка регистра и пробелов
- **Гибкий поиск**: Приоритет пользовательских словарей над стандартными
- **Обработка ошибок**: Корректная работа с пустыми строками и отсутствующими словами

**Структура файла `map_maker.py`:**
- `STANDARD_DICTIONARY`: Константа со стандартным словарем
- `get_definitions()`: Основная публичная функция
- Документация на русском языке с примерами использования

#### 3. Тесты (`test_map_maker.py`)
Комплексные тесты для модуля `map_maker.py`, покрывающие:
- Базовую функциональность
- Граничные случаи
- Обработку ошибок
- Unicode и специальные символы

## 🔧 Использование

### Запуск мониторинга
После запуска бот начнет мониторить задачи OpenHands и отправлять уведомления:

```
🤖 OpenHands Monitor Bot is online and starting to poll.
```

### Примеры уведомлений

**Новая задача:**
```
🆕 New Task Started: Реализация фичи X (ID: 12345)
```

**Изменение статуса:**
```
🔄 Task Status Update: Реализация фичи X is now COMPLETED.
```

### Использование модуля Map Maker

```python
from map_maker import get_definitions

# Использование стандартного словаря
definitions = get_definitions("apple")
print(definitions)  # ['A fruit that grows on trees', 'A technology company founded by Steve Jobs']

# Использование пользовательского словаря
custom_dict = {
    "python": ["Мой любимый язык программирования"],
    "openhands": ["Платформа для разработки ИИ"]
}
definitions = get_definitions("python", custom_dict)
print(definitions)  # ['Мой любимый язык программирования']
```

### 📚 Детальная документация функции `get_definitions()`

Функция `get_definitions()` является основной функцией модуля `map_maker.py` и предоставляет гибкий механизм для получения определений слов из различных источников.

#### Сигнатура функции
```python
def get_definitions(word: str, custom_dict: dict = None) -> list:
```

#### Параметры
- **`word`** (`str`): Слово для поиска определений. Обязательный параметр.
- **`custom_dict`** (`dict`, optional): Пользовательский словарь, где ключи - слова (строки), а значения - списки определений. Если не указан, используется стандартный словарь.

#### Возвращаемое значение
- **`list`**: Список строк с определениями слова. Если слово не найдено в словарях, возвращается пустой список `[]`.

#### Особенности работы
1. **Нормализация ввода**: Функция автоматически нормализует входное слово:
   - Приводит к нижнему регистру
   - Удаляет лишние пробелы с начала и конца
   - Пример: `"  Apple  "` → `"apple"`

2. **Приоритет поиска**: Если указан `custom_dict`, поиск выполняется сначала в пользовательском словаре, затем в стандартном.

3. **Стандартный словарь**: Включает предопределенные слова с их значениями:
   - `"apple"`: ["A fruit that grows on trees", "A technology company founded by Steve Jobs"]
   - `"python"`: ["A high-level programming language", "A large constricting snake"]
   - `"openhands"`: ["A platform for AI development and collaboration"]
   - `"test"`: ["A procedure intended to establish the quality...", "An examination of someone's knowledge..."]
   - `"hello"`: ["A greeting or expression of goodwill", "Used to attract attention"]
   - `"world"`: ["The earth, together with all of its countries...", "A particular region or group of countries"]

#### Примеры использования

**Базовый пример:**
```python
from map_maker import get_definitions

# Получение определений из стандартного словаря
result = get_definitions("python")
print(result)
# Output: ['A high-level programming language', 'A large constricting snake']
```

**С пользовательским словарем:**
```python
custom_dict = {
    "docker": ["Контейнеризация приложений", "Платформа для разработки"],
    "kubernetes": ["Оркестратор контейнеров", "Система управления кластерами"]
}

result = get_definitions("docker", custom_dict)
print(result)
# Output: ['Контейнеризация приложений', 'Платформа для разработки']
```

**Обработка отсутствующих слов:**
```python
result = get_definitions("nonexistentword")
print(result)
# Output: []
```

**Работа с различными форматами ввода:**
```python
# Разные регистры и пробелы
print(get_definitions("  APPLE  "))  # ['A fruit that grows on trees', 'A technology company...']
print(get_definitions("Python"))     # ['A high-level programming language', 'A large constricting snake']
print(get_definitions("HELLO"))      # ['A greeting or expression of goodwill', 'Used to attract attention']
```

#### Обработка ошибок
Функция корректно обрабатывает различные сценарии:
- **Пустая строка**: `get_definitions("")` → `[]`
- **Только пробелы**: `get_definitions("   ")` → `[]`
- **Нестроковые аргументы**: Вызовет ошибку времени выполнения

#### Расширение функциональности
Для расширения словаря можно:
1. **Использовать пользовательский словарь**: Передавать свой словарь как параметр
2. **Модифицировать стандартный словарь**: Изменить переменную `STANDARD_DICTIONARY` в файле `map_maker.py`
3. **Создать производный модуль**: Наследоваться от существующего функционала

#### Интеграция с другими компонентами
Функция `get_definitions()` может использоваться в различных сценариях:
- **Обогащение данных**: Добавление определений к ключевым словам
- **Поисковая система**: Поиск по определениям слов
- **Образовательные приложения**: Создание словарей и учебных материалов
- **Анализ текста**: Извлечение и классификация терминов

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

### Отчеты об ошибках
1. Проверьте существующие issues
2. Создайте новый issue с детальным описанием
3. Включите шаги для воспроизведения

### Запросы на добавление функциональности
1. Опишите предлагаемую функциональность
2. Объясните преимущества
3. Предложите реализацию

### Разработка
1. Создайте форк репозитория
2. Создайте ветку для вашей функции
3. Добавьте тесты
4. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле LICENSE.

## 📞 Поддержка

- **Issues**: [GitHub Issues](https://github.com/bughouse-wizzard/openhands-monitor-bot/issues)
- **Документация**: Этот README файл
- **Примеры**: См. раздел "Использование"

---

*Последнее обновление: 2026-01-06*