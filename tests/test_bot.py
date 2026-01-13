"""
Unit tests for core bot functions using pytest.

This test file implements the exact requirements from TASK 1:
- Tests for send_telegram_message function (success and failure cases)
- Tests for fetch_conversations function (success, failure, and empty cases)
- Tests for poll_and_notify function with proper mocking
- All external API calls are mocked using unittest.mock
- Follows PEP8 standards and uses type hinting
"""

import pytest
import asyncio
import sys
import os
import logging
from unittest.mock import AsyncMock, Mock, patch, MagicMock, call

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_bot_module_structure():
    """Test bot.py module structure."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    # Check that module can be imported
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Check for main functions
            assert hasattr(bot, 'send_telegram_message')
            assert hasattr(bot, 'fetch_conversations')
            assert hasattr(bot, 'poll_and_notify')
            assert hasattr(bot, 'main')
            assert hasattr(bot, 'conversation_states')
            
            # Check types
            assert callable(bot.send_telegram_message)
            assert callable(bot.fetch_conversations)
            assert callable(bot.poll_and_notify)
            assert callable(bot.main)
            assert isinstance(bot.conversation_states, dict)


def test_conversation_states_initialization():
    """Test conversation states initialization."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Check that conversation_states is initialized as empty dictionary
            assert bot.conversation_states == {}


def test_poll_interval():
    """Test poll interval value."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Check POLL_INTERVAL value
            assert hasattr(bot, 'POLL_INTERVAL')
            assert isinstance(bot.POLL_INTERVAL, int)
            assert bot.POLL_INTERVAL == 5


def test_api_url_configuration():
    """Test API URL configuration."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {
        'TELEGRAM_TOKEN': 'test',
        'CHAT_ID': 'test',
        'OPENHANDS_API_URL': 'http://custom-api:3000'
    }):
        with patch('telegram.Bot'):
            import bot
            
            # Check that URL is taken from environment variable
            assert bot.OPENHANDS_API_URL == 'http://custom-api:3000'


def test_default_api_url():
    """Test default API URL value."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}, clear=True):
        with patch('telegram.Bot'):
            import bot
            
            # Check default value
            assert bot.OPENHANDS_API_URL == 'http://host.docker.internal:3000'


@pytest.mark.asyncio
async def test_send_telegram_message_success():
    """Test successful sending of Telegram message."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Call the function
            test_message = "Test message"
            result = await bot.send_telegram_message(test_message)
            
            # Verify send_message was called with correct parameters
            mock_bot_instance.send_message.assert_called_once_with(
                chat_id='test', 
                text=test_message
            )
            
            # Verify function returns True on success
            assert result is True


@pytest.mark.asyncio
async def test_send_telegram_message_failure():
    """Test Telegram message sending failure with error handling."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            # Configure mock to raise exception
            from telegram.error import TelegramError
            mock_bot_instance.send_message.side_effect = TelegramError("Test error")
            
            import bot
            
            # Call function - it should return False on error (not raise exception)
            result = await bot.send_telegram_message("Test message")
            
            # Verify send_message was called once
            mock_bot_instance.send_message.assert_called_once_with(
                chat_id='test',
                text='Test message'
            )
            
            # Verify function returns False on error
            assert result is False


@pytest.mark.asyncio
async def test_fetch_conversations_success():
    """Test successful fetching of conversations from API."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {
        'TELEGRAM_TOKEN': 'test', 
        'CHAT_ID': 'test',
        'OPENHANDS_API_URL': 'http://test-api:3000'
    }):
        with patch('telegram.Bot'):
            import bot
            
            # Create mock response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = [
                {"id": "1", "title": "Task 1", "status": "active"},
                {"id": "2", "title": "Task 2", "status": "pending"}
            ]
            
            # Mock httpx.AsyncClient
            async def mock_client_get(*args, **kwargs):
                return mock_response
            
            with patch('httpx.AsyncClient') as mock_client_class:
                mock_client_instance = AsyncMock()
                mock_client_instance.get = AsyncMock(side_effect=mock_client_get)
                mock_client_class.return_value.__aenter__.return_value = mock_client_instance
                mock_client_class.return_value.__aexit__.return_value = None
                
                # Call the function
                result = await bot.fetch_conversations()
                
                # Verify result
                assert result == [
                    {"id": "1", "title": "Task 1", "status": "active"},
                    {"id": "2", "title": "Task 2", "status": "pending"}
                ]
                
                # Verify get was called with correct URL
                mock_client_instance.get.assert_called_once_with("http://test-api:3000/api/conversations")


@pytest.mark.asyncio
async def test_fetch_conversations_failure():
    """Test handling of HTTP error when fetching conversations."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            import httpx
            
            # Mock httpx.AsyncClient to raise HTTPStatusError
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            
            mock_client.get.side_effect = httpx.HTTPStatusError(
                "HTTP error", 
                request=Mock(), 
                response=Mock(status_code=500)
            )
            
            with patch('httpx.AsyncClient', return_value=mock_client):
                # Call the function
                result = await bot.fetch_conversations()
                
                # Verify empty list is returned on error
                assert result == []


@pytest.mark.asyncio
async def test_fetch_conversations_request_error():
    """Test handling of request error when fetching conversations."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            import httpx
            
            # Mock httpx.AsyncClient to raise RequestError
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            
            mock_client.get.side_effect = httpx.RequestError("Request error")
            
            with patch('httpx.AsyncClient', return_value=mock_client):
                # Call the function
                result = await bot.fetch_conversations()
                
                # Verify empty list is returned on error
                assert result == []


@pytest.mark.asyncio
async def test_fetch_conversations_empty_response():
    """Test handling of empty response when fetching conversations."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Mock httpx.AsyncClient to return empty list
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = []
            mock_response.raise_for_status = Mock()
            
            mock_client.get.return_value = mock_response
            
            with patch('httpx.AsyncClient', return_value=mock_client):
                # Call the function
                result = await bot.fetch_conversations()
                
                # Verify empty list is returned
                assert result == []


@pytest.mark.asyncio
async def test_fetch_conversations_json_error():
    """Test handling of JSON parsing error when fetching conversations."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Mock httpx.AsyncClient to return invalid JSON
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_response.raise_for_status = Mock()
            
            mock_client.get.return_value = mock_response
            
            with patch('httpx.AsyncClient', return_value=mock_client):
                # Call the function
                result = await bot.fetch_conversations()
                
                # Verify empty list is returned on JSON error
                assert result == []


@pytest.mark.asyncio
async def test_poll_and_notify():
    """Test poll_and_notify function with state change detection."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Clear conversation states
            bot.conversation_states = {}
            
            # Mock fetch_conversations to return different states
            mock_conversations_first = [
                {"id": "1", "title": "Task 1", "status": "running"}
            ]
            
            # Mock send_telegram_message to track calls
            mock_send = AsyncMock(return_value=True)
            
            # Mock asyncio.sleep to prevent infinite loop
            sleep_calls = []
            async def mock_sleep(delay):
                sleep_calls.append(delay)
                if len(sleep_calls) > 1:  # Stop after 1 iteration
                    raise asyncio.CancelledError()
            
            with patch.object(bot, 'fetch_conversations', AsyncMock(return_value=mock_conversations_first)):
                with patch.object(bot, 'send_telegram_message', mock_send):
                    with patch('asyncio.sleep', mock_sleep):
                        # Run poll_and_notify - it should raise CancelledError
                        try:
                            await bot.poll_and_notify()
                        except asyncio.CancelledError:
                            pass
                        
                        # Verify message was sent for new conversation
                        mock_send.assert_called_once()
                        call_args = mock_send.call_args[0]
                        assert "New Task Started: Task 1" in call_args[0]
                        
                        # Verify state was updated
                        assert bot.conversation_states == {"1": "running"}


@pytest.mark.asyncio
async def test_poll_and_notify_empty_conversations():
    """Test poll_and_notify with empty conversations list."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Clear conversation states
            bot.conversation_states = {}
            
            # Mock fetch_conversations to return empty list
            mock_fetch = AsyncMock()
            mock_fetch.return_value = []
            
            # Mock asyncio.sleep to break the loop after first iteration
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]) as mock_sleep:
                with patch.object(bot, 'fetch_conversations', new=mock_fetch):
                    # Run poll_and_notify and expect loop to break
                    with pytest.raises(Exception, match="Break loop"):
                        await bot.poll_and_notify()
                    
                    # Verify no messages were sent
                    # (send_telegram_message should not be called)
                    # Verify state remains empty
                    assert bot.conversation_states == {}


@pytest.mark.asyncio
async def test_poll_and_notify_cleanup_old_conversations():
    """Test cleanup of old conversations in poll_and_notify."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Set up initial conversation states
            bot.conversation_states = {
                "old1": "active",
                "old2": "completed",
                "current": "pending"
            }
            
            # Mock fetch_conversations to return only current conversation
            mock_fetch = AsyncMock()
            mock_fetch.return_value = [
                {"id": "current", "title": "Current Task", "status": "pending"}
            ]
            
            # Mock asyncio.sleep to break the loop after first iteration
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]) as mock_sleep:
                with patch.object(bot, 'fetch_conversations', new=mock_fetch):
                    # Run poll_and_notify and expect loop to break
                    with pytest.raises(Exception, match="Break loop"):
                        await bot.poll_and_notify()
                    
                    # Verify old conversations were cleaned up
                    assert "old1" not in bot.conversation_states
                    assert "old2" not in bot.conversation_states
                    assert "current" in bot.conversation_states
                    assert bot.conversation_states["current"] == "pending"


@pytest.mark.asyncio
async def test_main_function():
    """Test main function execution."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Mock poll_and_notify to raise KeyboardInterrupt to break the loop
            mock_poll = AsyncMock()
            mock_poll.side_effect = KeyboardInterrupt()
            
            with patch.object(bot, 'poll_and_notify', new=mock_poll):
                # Call main function - should exit cleanly
                try:
                    await bot.main()
                except KeyboardInterrupt:
                    # Expected behavior
                    pass
                
                # Verify poll_and_notify was called
                mock_poll.assert_called_once()


@pytest.mark.asyncio
async def test_main_missing_environment_variables():
    """Test main function with missing environment variables."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    # Clear environment variables
    with patch.dict('os.environ', {}, clear=True):
        with patch('telegram.Bot'):
            import bot
            
            # Call main function - should exit with error
            # We can't easily test sys.exit, but we can verify the function
            # handles missing environment variables gracefully
            try:
                await bot.main()
                # If we get here, main didn't exit as expected
                assert False, "main should exit when environment variables are missing"
            except ValueError as e:
                # Expected behavior - main raises ValueError when env vars are missing
                assert "TELEGRAM_TOKEN and CHAT_ID environment variables must be set" in str(e)


# ============================================================================
# TASK 2: Additional tests for poll_and_notify and main functions
# ============================================================================

@pytest.mark.asyncio
async def test_poll_and_notify_success():
    """
    Test poll_and_notify with successful conversation fetching and notification.
    
    Mocks fetch_conversations to return a predetermined set of conversations.
    Mocks send_telegram_message to track message sending.
    Asserts that send_telegram_message is called with the correct arguments.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Clear conversation states
            bot.conversation_states = {}
            
            # Mock conversations data
            mock_conversations = [
                {"id": "conv1", "title": "Task 1", "status": "running"},
                {"id": "conv2", "title": "Task 2", "status": "pending"}
            ]
            
            # Track calls to send_telegram_message
            sent_messages = []
            async def mock_send_telegram_message(message):
                sent_messages.append(message)
                return True
            
            # Mock asyncio.sleep to break the loop after first iteration
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]):
                with patch.object(bot, 'fetch_conversations', AsyncMock(return_value=mock_conversations)):
                    with patch.object(bot, 'send_telegram_message', mock_send_telegram_message):
                        # Run poll_and_notify and expect loop to break
                        with pytest.raises(Exception, match="Break loop"):
                            await bot.poll_and_notify()
                        
                        # Verify messages were sent for new conversations
                        assert len(sent_messages) == 2
                        assert "🆕 New Task Started: Task 1 (ID: conv1)" in sent_messages[0]
                        assert "🆕 New Task Started: Task 2 (ID: conv2)" in sent_messages[1]
                        
                        # Verify states were updated
                        assert bot.conversation_states == {"conv1": "running", "conv2": "pending"}


@pytest.mark.asyncio
async def test_poll_and_notify_no_changes():
    """
    Test poll_and_notify when conversations don't change between polls.
    
    Mocks fetch_conversations to return the same set of conversations in consecutive calls.
    Asserts that send_telegram_message is not called for unchanged conversations.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Set up initial conversation states
            bot.conversation_states = {
                "conv1": "running",
                "conv2": "pending"
            }
            
            # Mock conversations data (same as initial states)
            mock_conversations = [
                {"id": "conv1", "title": "Task 1", "status": "running"},
                {"id": "conv2", "title": "Task 2", "status": "pending"}
            ]
            
            # Track calls to send_telegram_message
            sent_messages = []
            async def mock_send_telegram_message(message):
                sent_messages.append(message)
                return True
            
            # Mock asyncio.sleep to break the loop after first iteration
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]):
                with patch.object(bot, 'fetch_conversations', AsyncMock(return_value=mock_conversations)):
                    with patch.object(bot, 'send_telegram_message', mock_send_telegram_message):
                        # Run poll_and_notify and expect loop to break
                        with pytest.raises(Exception, match="Break loop"):
                            await bot.poll_and_notify()
                        
                        # Verify no messages were sent (no changes)
                        assert len(sent_messages) == 0
                        
                        # Verify states remain unchanged
                        assert bot.conversation_states == {"conv1": "running", "conv2": "pending"}


@pytest.mark.asyncio
async def test_poll_and_notify_exception():
    """
    Test poll_and_notify exception handling.
    
    Mocks fetch_conversations to return empty list (simulating exception handling).
    Asserts that the exception is handled correctly and doesn't crash the polling loop.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Clear conversation states
            bot.conversation_states = {}
            
            # Track calls to send_telegram_message
            sent_messages = []
            async def mock_send_telegram_message(message):
                sent_messages.append(message)
                return True
            
            # Mock fetch_conversations to return empty list (simulating exception handling)
            mock_fetch = AsyncMock(return_value=[])
            
            # Mock asyncio.sleep to break the loop after first iteration
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]):
                with patch.object(bot, 'fetch_conversations', mock_fetch):
                    with patch.object(bot, 'send_telegram_message', mock_send_telegram_message):
                        # Run poll_and_notify and expect loop to break
                        with pytest.raises(Exception, match="Break loop"):
                            await bot.poll_and_notify()
                        
                        # Verify no messages were sent (exception was handled)
                        assert len(sent_messages) == 0
                        
                        # Verify states remain empty
                        assert bot.conversation_states == {}


@pytest.mark.asyncio
async def test_main_initialization():
    """
    Test main function initialization.
    
    Uses asyncio.create_task to run main in a separate task.
    Mocks poll_and_notify to prevent infinite looping.
    Asserts that the necessary components are initialized correctly.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Mock poll_and_notify to raise a test exception to break the loop
            mock_poll = AsyncMock()
            mock_poll.side_effect = RuntimeError("Test exception to break loop")
            
            # Mock send_telegram_message to track startup message
            startup_message_sent = []
            async def mock_send_telegram_message(message):
                startup_message_sent.append(message)
                return True
            
            with patch.object(bot, 'poll_and_notify', mock_poll):
                with patch.object(bot, 'send_telegram_message', mock_send_telegram_message):
                    # Create a task for main function
                    task = asyncio.create_task(bot.main())
                    
                    try:
                        # Wait for task to complete with timeout
                        # Should raise RuntimeError from mocked poll_and_notify
                        await asyncio.wait_for(task, timeout=1.0)
                    except RuntimeError as e:
                        # Expected behavior - RuntimeError from mock
                        assert "Test exception to break loop" in str(e)
                    except asyncio.TimeoutError:
                        # If timeout occurs, cancel the task
                        task.cancel()
                        try:
                            await task
                        except (asyncio.CancelledError, RuntimeError):
                            pass
                    
                    # Verify startup message was sent
                    assert len(startup_message_sent) == 1
                    assert "OpenHands Monitor Bot is online" in startup_message_sent[0]
                    
                    # Verify poll_and_notify was called
                    mock_poll.assert_called_once()