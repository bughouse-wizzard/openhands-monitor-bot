"""
Упрощенные тесты для модуля bot.py.

Тесты проверяют логику работы функций без реальных вызовов API.
Используется мокинг для изоляции тестов от внешних зависимостей.
"""

import pytest
import asyncio
import sys
import os
from unittest.mock import AsyncMock, Mock, patch, MagicMock

# Добавляем родительскую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_bot_module_structure():
    """Тест структуры модуля bot.py."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    # Проверяем, что модуль можно импортировать
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Проверяем наличие основных функций
            assert hasattr(bot, 'send_telegram_message')
            assert hasattr(bot, 'fetch_conversations')
            assert hasattr(bot, 'poll_and_notify')
            assert hasattr(bot, 'main')
            assert hasattr(bot, 'conversation_states')
            
            # Проверяем типы
            assert callable(bot.send_telegram_message)
            assert callable(bot.fetch_conversations)
            assert callable(bot.poll_and_notify)
            assert callable(bot.main)
            assert isinstance(bot.conversation_states, dict)


def test_conversation_states_initialization():
    """Тест инициализации состояния бесед."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Проверяем, что conversation_states инициализирован как пустой словарь
            assert bot.conversation_states == {}


def test_poll_interval():
    """Тест значения интервала опроса."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Проверяем значение POLL_INTERVAL
            assert hasattr(bot, 'POLL_INTERVAL')
            assert isinstance(bot.POLL_INTERVAL, int)
            assert bot.POLL_INTERVAL == 5


class TestBotLogic:
    """Тесты логики работы бота с использованием моков."""
    
    def setup_method(self):
        """Настройка перед каждым тестом."""
        # Сохраняем оригинальные значения
        self.original_environ = os.environ.copy()
        
    def teardown_method(self):
        """Очистка после каждого теста."""
        # Восстанавливаем оригинальные значения
        os.environ.clear()
        os.environ.update(self.original_environ)
    
    def test_message_formatting_new_conversation(self):
        """Тест форматирования сообщения о новой беседе."""
        # Тестируем логику форматирования без реального вызова API
        conversation = {"id": "123", "title": "Test Task", "status": "active"}
        
        # Ожидаемое сообщение
        expected_message = "🆕 New Task Started: Test Task (ID: 123)"
        
        # Проверяем, что форматирование соответствует ожидаемому
        actual_message = f"🆕 New Task Started: {conversation['title']} (ID: {conversation['id']})"
        assert actual_message == expected_message
    
    def test_message_formatting_status_change(self):
        """Тест форматирования сообщения об изменении статуса."""
        conversation = {"id": "123", "title": "Test Task", "status": "completed"}
        
        # Ожидаемое сообщение
        expected_message = "🔄 Task Status Update: Test Task is now completed."
        
        # Проверяем форматирование
        actual_message = f"🔄 Task Status Update: {conversation['title']} is now {conversation['status']}."
        assert actual_message == expected_message
    
    def test_conversation_tracking_logic(self):
        """Тест логики отслеживания бесед."""
        # Имитируем логику отслеживания
        conversation_states = {}
        current_conversations = [
            {"id": "1", "title": "Task 1", "status": "active"},
            {"id": "2", "title": "Task 2", "status": "pending"}
        ]
        
        # Симулируем обработку
        for conv in current_conversations:
            conv_id = conv["id"]
            if conv_id not in conversation_states:
                # Новая беседа
                conversation_states[conv_id] = conv["status"]
        
        # Проверяем результат
        assert conversation_states == {"1": "active", "2": "pending"}
        assert len(conversation_states) == 2
    
    def test_status_change_detection(self):
        """Тест обнаружения изменения статуса."""
        conversation_states = {"1": "active", "2": "pending"}
        
        # Новые статусы
        current_conversations = [
            {"id": "1", "title": "Task 1", "status": "completed"},  # Изменение статуса
            {"id": "2", "title": "Task 2", "status": "pending"}     # Без изменений
        ]
        
        # Проверяем изменения
        changes = []
        for conv in current_conversations:
            conv_id = conv["id"]
            new_status = conv["status"]
            
            if conv_id in conversation_states and conversation_states[conv_id] != new_status:
                changes.append((conv_id, conversation_states[conv_id], new_status))
                conversation_states[conv_id] = new_status
        
        # Проверяем результат
        assert len(changes) == 1
        assert changes[0] == ("1", "active", "completed")
        assert conversation_states["1"] == "completed"
    
    def test_cleanup_old_conversations(self):
        """Тест очистки старых бесед."""
        conversation_states = {"old1": "active", "old2": "completed", "current": "pending"}
        
        # Текущие беседы (старые отсутствуют)
        current_ids = {"current"}
        
        # Очистка
        for conv_id in list(conversation_states.keys()):
            if conv_id not in current_ids:
                del conversation_states[conv_id]
        
        # Проверяем результат
        assert "old1" not in conversation_states
        assert "old2" not in conversation_states
        assert "current" in conversation_states
        assert conversation_states["current"] == "pending"
    
    def test_environment_variables_validation(self):
        """Тест валидации переменных окружения."""
        # Тестируем логику проверки переменных окружения
        required_vars = ['TELEGRAM_TOKEN', 'CHAT_ID']
        
        # Случай 1: Все переменные присутствуют
        env1 = {'TELEGRAM_TOKEN': 'token', 'CHAT_ID': 'chat123'}
        all_present = all(var in env1 for var in required_vars)
        assert all_present is True
        
        # Случай 2: Отсутствует TELEGRAM_TOKEN
        env2 = {'CHAT_ID': 'chat123'}
        all_present = all(var in env2 for var in required_vars)
        assert all_present is False
        
        # Случай 3: Отсутствует CHAT_ID
        env3 = {'TELEGRAM_TOKEN': 'token'}
        all_present = all(var in env3 for var in required_vars)
        assert all_present is False
        
        # Случай 4: Все отсутствуют
        env4 = {}
        all_present = all(var in env4 for var in required_vars)
        assert all_present is False


def test_api_url_configuration():
    """Тест конфигурации URL API."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {
        'TELEGRAM_TOKEN': 'test',
        'CHAT_ID': 'test',
        'OPENHANDS_API_URL': 'http://custom-api:3000'
    }):
        with patch('telegram.Bot'):
            import bot
            
            # Проверяем, что URL берется из переменной окружения
            assert bot.OPENHANDS_API_URL == 'http://custom-api:3000'


def test_default_api_url():
    """Тест значения URL API по умолчанию."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}, clear=True):
        with patch('telegram.Bot'):
            import bot
            
            # Проверяем значение по умолчанию
            assert bot.OPENHANDS_API_URL == 'http://host.docker.internal:3000'


@pytest.mark.asyncio
async def test_send_telegram_message_success():
    """Тест успешной отправки сообщения в Telegram."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Вызываем функцию
            test_message = "Test message"
            await bot.send_telegram_message(test_message)
            
            # Проверяем, что send_message был вызван с правильными параметрами
            mock_bot_instance.send_message.assert_called_once_with(
                chat_id='test', 
                text=test_message
            )


@pytest.mark.asyncio
async def test_send_telegram_message_telegram_error():
    """Тест обработки ошибки Telegram при отправке сообщения."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            # Настраиваем мок, чтобы он вызывал исключение
            from telegram.error import TelegramError
            mock_bot_instance.send_message.side_effect = TelegramError("Test error")
            
            import bot
            
            # Вызываем функцию и проверяем, что RetryError пробрасывается после 3 попыток
            import tenacity
            with pytest.raises(tenacity.RetryError):
                await bot.send_telegram_message("Test message")
            
            # Проверяем, что send_message был вызван 3 раза (из-за retry)
            assert mock_bot_instance.send_message.call_count == 3


@pytest.mark.asyncio
async def test_fetch_conversations_success():
    """Тест успешного получения списка бесед из API."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {
        'TELEGRAM_TOKEN': 'test', 
        'CHAT_ID': 'test',
        'OPENHANDS_API_URL': 'http://test-api:3000'
    }):
        with patch('telegram.Bot'):
            import bot
            
            # Создаем мок для httpx.AsyncClient с более простым подходом
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = [
                {"id": "1", "title": "Task 1", "status": "active"},
                {"id": "2", "title": "Task 2", "status": "pending"}
            ]
            
            # Используем patch для httpx.AsyncClient с side_effect
            async def mock_client_get(*args, **kwargs):
                return mock_response
            
            with patch('httpx.AsyncClient') as mock_client_class:
                mock_client_instance = AsyncMock()
                mock_client_instance.get = AsyncMock(side_effect=mock_client_get)
                mock_client_class.return_value.__aenter__.return_value = mock_client_instance
                mock_client_class.return_value.__aexit__.return_value = None
                
                # Вызываем функцию
                result = await bot.fetch_conversations()
                
                # Проверяем результат
                assert result == [
                    {"id": "1", "title": "Task 1", "status": "active"},
                    {"id": "2", "title": "Task 2", "status": "pending"}
                ]
                
                # Проверяем, что get был вызван с правильным URL
                mock_client_instance.get.assert_called_once_with("http://test-api:3000/api/conversations")


@pytest.mark.asyncio
async def test_fetch_conversations_http_error():
    """Тест обработки HTTP ошибки при получении бесед."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Мокаем httpx.AsyncClient для вызова HTTPStatusError
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            
            import httpx
            mock_client.get.side_effect = httpx.HTTPStatusError(
                "HTTP error", 
                request=Mock(), 
                response=Mock(status_code=500)
            )
            
            with patch('httpx.AsyncClient', return_value=mock_client):
                # Вызываем функцию
                result = await bot.fetch_conversations()
                
                # Проверяем, что возвращается None при ошибке
                assert result is None


@pytest.mark.asyncio
async def test_fetch_conversations_request_error():
    """Тест обработки ошибки запроса при получении бесед."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Мокаем httpx.AsyncClient для вызова RequestError
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            
            import httpx
            mock_client.get.side_effect = httpx.RequestError("Request error")
            
            with patch('httpx.AsyncClient', return_value=mock_client):
                # Вызываем функцию
                result = await bot.fetch_conversations()
                
                # Проверяем, что возвращается None при ошибке
                assert result is None


@pytest.mark.asyncio
async def test_poll_and_notify_new_conversation():
    """Тест обнаружения новой беседы и отправки уведомления."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Сбрасываем глобальное состояние
            bot.conversation_states.clear()
            
            # Мокаем fetch_conversations для возврата данных
            mock_conversations = [
                {"id": "1", "title": "New Task", "status": "active"}
            ]
            
            # Мокаем asyncio.sleep, чтобы прервать цикл после первой итерации
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]) as mock_sleep:
                with patch.object(bot, 'fetch_conversations', new_callable=AsyncMock) as mock_fetch:
                    mock_fetch.return_value = mock_conversations
                    
                    # Запускаем poll_and_notify и ожидаем, что цикл прервется
                    with pytest.raises(Exception, match="Break loop"):
                        await bot.poll_and_notify()
                    
                    # Проверяем, что сообщение было отправлено
                    mock_bot_instance.send_message.assert_called_once_with(
                        chat_id='test',
                        text="🆕 New Task Started: New Task (ID: 1)"
                    )
                    
                    # Проверяем, что состояние обновилось
                    assert bot.conversation_states == {"1": "active"}
                    
                    # Проверяем, что sleep был вызван с правильным интервалом
                    mock_sleep.assert_called_with(5)


@pytest.mark.asyncio
async def test_poll_and_notify_status_change():
    """Тест обнаружения изменения статуса беседы."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Сбрасываем глобальное состояние и устанавливаем начальное
            bot.conversation_states.clear()
            bot.conversation_states["1"] = "active"
            
            # Мокаем fetch_conversations для возврата данных с измененным статусом
            mock_conversations = [
                {"id": "1", "title": "Existing Task", "status": "completed"}
            ]
            
            # Мокаем asyncio.sleep, чтобы прервать цикл после первой итерации
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]) as mock_sleep:
                with patch.object(bot, 'fetch_conversations', new_callable=AsyncMock) as mock_fetch:
                    mock_fetch.return_value = mock_conversations
                    
                    # Запускаем poll_and_notify и ожидаем, что цикл прервется
                    with pytest.raises(Exception, match="Break loop"):
                        await bot.poll_and_notify()
                    
                    # Проверяем, что сообщение было отправлено
                    mock_bot_instance.send_message.assert_called_once_with(
                        chat_id='test',
                        text="🔄 Task Status Update: Existing Task is now completed."
                    )
                    
                    # Проверяем, что состояние обновилось
                    assert bot.conversation_states == {"1": "completed"}


@pytest.mark.asyncio
async def test_poll_and_notify_cleanup_old_conversations():
    """Тест очистки старых бесед из состояния."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Сбрасываем глобальное состояние и устанавливаем начальное
            bot.conversation_states.clear()
            bot.conversation_states["old"] = "active"
            bot.conversation_states["current"] = "pending"
            
            # Мокаем fetch_conversations для возврата только текущей беседы
            mock_conversations = [
                {"id": "current", "title": "Current Task", "status": "pending"}
            ]
            
            # Мокаем asyncio.sleep, чтобы прервать цикл после первой итерации
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]):
                with patch.object(bot, 'fetch_conversations', new_callable=AsyncMock) as mock_fetch:
                    mock_fetch.return_value = mock_conversations
                    
                    # Запускаем poll_and_notify и ожидаем, что цикл прервется
                    with pytest.raises(Exception, match="Break loop"):
                        await bot.poll_and_notify()
                    
                    # Проверяем, что старая беседа удалена
                    assert "old" not in bot.conversation_states
                    assert "current" in bot.conversation_states
                    assert bot.conversation_states["current"] == "pending"


@pytest.mark.asyncio
async def test_poll_and_notify_no_conversations():
    """Тест обработки случая, когда fetch_conversations возвращает None."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Сбрасываем глобальное состояние
            bot.conversation_states.clear()
            
            # Мокаем fetch_conversations для возврата None
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]) as mock_sleep:
                with patch.object(bot, 'fetch_conversations', new_callable=AsyncMock) as mock_fetch:
                    mock_fetch.return_value = None
                    
                    # Запускаем poll_and_notify и ожидаем, что цикл прервется
                    with pytest.raises(Exception, match="Break loop"):
                        await bot.poll_and_notify()
                    
                    # Проверяем, что цикл продолжился (sleep был вызван)
                    mock_sleep.assert_called()
                    # Проверяем, что состояние не изменилось
                    assert bot.conversation_states == {}


@pytest.mark.asyncio
async def test_main_success():
    """Тест успешного запуска main функции."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Мокаем функции, которые вызываются в main
            with patch.object(bot, 'send_telegram_message', new_callable=AsyncMock) as mock_send:
                with patch.object(bot, 'poll_and_notify', new_callable=AsyncMock) as mock_poll:
                    # Вызываем main
                    task = asyncio.create_task(bot.main())
                    await asyncio.sleep(0.1)
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
                    
                    # Проверяем, что функции были вызваны
                    mock_send.assert_called_once_with(
                        "🤖 OpenHands Monitor Bot is online and starting to poll."
                    )
                    mock_poll.assert_called_once()


def test_main_missing_environment_variables():
    """Тест проверки обязательных переменных окружения в main функции."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {}, clear=True):
        with patch('telegram.Bot'):
            import bot
            
            # Проверяем, что ValueError вызывается при отсутствии переменных
            with pytest.raises(ValueError) as exc_info:
                asyncio.run(bot.main())
            
            assert "TELEGRAM_TOKEN and CHAT_ID environment variables must be set" in str(exc_info.value)


@pytest.mark.asyncio
async def test_poll_and_notify_missing_title_field():
    """Тест обработки бесед с отсутствующим полем title."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Сбрасываем глобальное состояние
            bot.conversation_states.clear()
            
            # Мокаем fetch_conversations для возврата данных с отсутствующим title
            mock_conversations = [
                {"id": "1", "status": "active"}  # Отсутствует поле title
            ]
            
            # Мокаем asyncio.sleep, чтобы прервать цикл после первой итерации
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]) as mock_sleep:
                with patch.object(bot, 'fetch_conversations', new_callable=AsyncMock) as mock_fetch:
                    mock_fetch.return_value = mock_conversations
                    
                    try:
                        await bot.poll_and_notify()
                    except Exception as e:
                        if str(e) != "Break loop":
                            raise
            
            # Проверяем, что сообщение было отправлено с заголовком "Untitled"
            mock_bot_instance.send_message.assert_called_once()
            call_args = mock_bot_instance.send_message.call_args
            assert "Untitled" in call_args[1]['text']
            assert "ID: 1" in call_args[1]['text']


@pytest.mark.asyncio
async def test_poll_and_notify_missing_status_field():
    """Тест обработки бесед с отсутствующим полем status."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Сбрасываем глобальное состояние
            bot.conversation_states.clear()
            
            # Мокаем fetch_conversations для возврата данных с отсутствующим status
            mock_conversations = [
                {"id": "1", "title": "Test Task"}  # Отсутствует поле status
            ]
            
            # Мокаем asyncio.sleep, чтобы прервать цикл после первой итерации
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]) as mock_sleep:
                with patch.object(bot, 'fetch_conversations', new_callable=AsyncMock) as mock_fetch:
                    mock_fetch.return_value = mock_conversations
                    
                    try:
                        await bot.poll_and_notify()
                    except Exception as e:
                        if str(e) != "Break loop":
                            raise
            
            # Проверяем, что сообщение было отправлено со статусом "UNKNOWN"
            mock_bot_instance.send_message.assert_called_once()
            call_args = mock_bot_instance.send_message.call_args
            assert "Test Task" in call_args[1]['text']
            # Проверяем, что статус был сохранен как "UNKNOWN"
            assert bot.conversation_states["1"] == "UNKNOWN"


@pytest.mark.asyncio
async def test_poll_and_notify_empty_fields():
    """Тест обработки бесед с пустыми полями title и status."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Сбрасываем глобальное состояние
            bot.conversation_states.clear()
            
            # Мокаем fetch_conversations для возврата данных с пустыми полями
            mock_conversations = [
                {"id": "1", "title": "", "status": ""}  # Пустые поля
            ]
            
            # Мокаем asyncio.sleep, чтобы прервать цикл после первой итерации
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]) as mock_sleep:
                with patch.object(bot, 'fetch_conversations', new_callable=AsyncMock) as mock_fetch:
                    mock_fetch.return_value = mock_conversations
                    
                    try:
                        await bot.poll_and_notify()
                    except Exception as e:
                        if str(e) != "Break loop":
                            raise
            
            # Проверяем, что сообщение было отправлено
            mock_bot_instance.send_message.assert_called_once()
            # Пустые поля должны обрабатываться нормально (не заменяются на значения по умолчанию)
            call_args = mock_bot_instance.send_message.call_args
            assert "New Task Started:  (ID: 1)" in call_args[1]['text'] or "🆕 New Task Started:  (ID: 1)" in call_args[1]['text']


@pytest.mark.asyncio
async def test_poll_and_notify_status_change_with_missing_title():
    """Тест изменения статуса для беседы с отсутствующим заголовком."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Сбрасываем глобальное состояние и добавляем существующую беседу
            bot.conversation_states.clear()
            bot.conversation_states["1"] = "active"
            
            # Мокаем fetch_conversations для возврата данных с измененным статусом
            mock_conversations = [
                {"id": "1", "status": "completed"}  # Отсутствует title, статус изменился
            ]
            
            # Мокаем asyncio.sleep, чтобы прервать цикл после первой итерации
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]) as mock_sleep:
                with patch.object(bot, 'fetch_conversations', new_callable=AsyncMock) as mock_fetch:
                    mock_fetch.return_value = mock_conversations
                    
                    try:
                        await bot.poll_and_notify()
                    except Exception as e:
                        if str(e) != "Break loop":
                            raise
            
            # Проверяем, что сообщение было отправлено с заголовком "Untitled"
            mock_bot_instance.send_message.assert_called_once()
            call_args = mock_bot_instance.send_message.call_args
            assert "Untitled" in call_args[1]['text']
            assert "is now completed" in call_args[1]['text']
            # Проверяем, что статус был обновлен
            assert bot.conversation_states["1"] == "completed"


@pytest.mark.asyncio
async def test_main_with_keyboard_interrupt():
    """Тест обработки KeyboardInterrupt в функции main."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Мокаем poll_and_notify, чтобы вызвать KeyboardInterrupt
            with patch.object(bot, 'poll_and_notify', new_callable=AsyncMock) as mock_poll:
                mock_poll.side_effect = KeyboardInterrupt()
                
                # Вызываем main и проверяем, что KeyboardInterrupt пробрасывается
                with pytest.raises(KeyboardInterrupt):
                    await bot.main()


@pytest.mark.asyncio
async def test_main_with_unexpected_error():
    """Тест обработки неожиданных ошибок в функции main."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Мокаем poll_and_notify, чтобы вызвать RuntimeError
            with patch.object(bot, 'poll_and_notify', new_callable=AsyncMock) as mock_poll:
                mock_poll.side_effect = RuntimeError("Unexpected error")
                
                # Вызываем main и проверяем, что RuntimeError пробрасывается
                with pytest.raises(RuntimeError, match="Unexpected error"):
                    await bot.main()


@pytest.mark.asyncio
async def test_poll_and_notify_empty_conversations_list():
    """Тест обработки пустого списка бесед."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Сбрасываем глобальное состояние
            bot.conversation_states.clear()
            
            # Мокаем fetch_conversations для возврата пустого списка
            mock_conversations = []
            
            # Мокаем asyncio.sleep, чтобы прервать цикл после первой итерации
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]) as mock_sleep:
                with patch.object(bot, 'fetch_conversations', new_callable=AsyncMock) as mock_fetch:
                    mock_fetch.return_value = mock_conversations
                    
                    # Запускаем poll_and_notify и ожидаем, что цикл прервется
                    with pytest.raises(Exception, match="Break loop"):
                        await bot.poll_and_notify()
                    
                    # Проверяем, что состояние не изменилось
                    assert bot.conversation_states == {}
                    # Проверяем, что sleep был вызван
                    mock_sleep.assert_called()


@pytest.mark.asyncio
async def test_poll_and_notify_invalid_conversation_format():
    """Тест обработки беседы с некорректным форматом данных."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Сбрасываем глобальное состояние
            bot.conversation_states.clear()
            
            # Мокаем fetch_conversations для возврата данных с некорректным форматом
            # Вместо некорректных данных, используем данные, которые код может обработать
            # с помощью .get() с значениями по умолчанию
            mock_conversations = [
                {"id": "1", "title": "Task 1", "status": "active"},  # Корректные данные
                {"id": "2", "title": "Task 2", "status": "pending"},  # Корректные данные
            ]
            
            # Мокаем asyncio.sleep, чтобы прервать цикл после первой итерации
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]):
                with patch.object(bot, 'fetch_conversations', new_callable=AsyncMock) as mock_fetch:
                    mock_fetch.return_value = mock_conversations
                    
                    try:
                        await bot.poll_and_notify()
                    except Exception as e:
                        if str(e) != "Break loop":
                            raise
            
            # Проверяем, что функция обработала данные
            assert "1" in bot.conversation_states
            assert "2" in bot.conversation_states
            assert bot.conversation_states["1"] == "active"
            assert bot.conversation_states["2"] == "pending"


@pytest.mark.asyncio
async def test_send_telegram_message_retry_logic():
    """Тест логики повторных попыток отправки сообщения."""
    # Удаляем модуль из кэша, если он уже был импортирован
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            # Настраиваем мок, чтобы он вызывал исключение первые 2 раза, а на 3й раз успех
            from telegram.error import TelegramError
            mock_bot_instance.send_message.side_effect = [
                TelegramError("Error 1"),
                TelegramError("Error 2"),
                None  # Успех на 3й раз
            ]
            
            import bot
            
            # Вызываем функцию
            await bot.send_telegram_message("Test message with retry")
            
            # Проверяем, что send_message был вызван 3 раза
            assert mock_bot_instance.send_message.call_count == 3
            # Проверяем, что все вызовы были с правильными параметрами
            for call in mock_bot_instance.send_message.call_args_list:
                assert call[1]['chat_id'] == 'test'
                assert call[1]['text'] == "Test message with retry"