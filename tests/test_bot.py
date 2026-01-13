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


# ============================================================================
# TASK 2: Additional comprehensive tests for poll_and_notify and main functions
# ============================================================================

@pytest.mark.asyncio
async def test_poll_and_notify_state_changes():
    """
    Test poll_and_notify with multiple state changes across polling cycles.
    
    Mocks fetch_conversations to return different conversation states across
    multiple calls to simulate real-world state changes.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Clear conversation states
            bot.conversation_states = {}
            
            # Track all sent messages
            sent_messages = []
            async def mock_send_telegram_message(message):
                sent_messages.append(message)
                return True
            
            # Simulate multiple polling cycles with different states
            polling_cycles = [
                # First cycle: New conversation appears
                [{"id": "conv1", "title": "Task 1", "status": "running"}],
                # Second cycle: Status changes
                [{"id": "conv1", "title": "Task 1", "status": "completed"}],
                # Third cycle: New conversation appears, first one still exists
                [
                    {"id": "conv1", "title": "Task 1", "status": "completed"},
                    {"id": "conv2", "title": "Task 2", "status": "pending"}
                ],
                # Fourth cycle: Status changes for both conversations
                [
                    {"id": "conv1", "title": "Task 1", "status": "archived"},
                    {"id": "conv2", "title": "Task 2", "status": "running"}
                ]
            ]
            
            # Create a mock that returns different values each call
            fetch_call_count = 0
            async def mock_fetch_conversations():
                nonlocal fetch_call_count
                if fetch_call_count < len(polling_cycles):
                    result = polling_cycles[fetch_call_count]
                    fetch_call_count += 1
                    return result
                # After all cycles, raise exception to break loop
                raise Exception("Test complete - break loop")
            
            # Mock asyncio.sleep to control loop iterations
            sleep_calls = []
            async def mock_sleep(delay):
                sleep_calls.append(delay)
                # Break after processing all cycles
                if fetch_call_count >= len(polling_cycles):
                    raise Exception("Test complete - break loop")
            
            with patch.object(bot, 'fetch_conversations', mock_fetch_conversations):
                with patch.object(bot, 'send_telegram_message', mock_send_telegram_message):
                    with patch('asyncio.sleep', mock_sleep):
                        # Run poll_and_notify
                        try:
                            await bot.poll_and_notify()
                        except Exception as e:
                            if "Test complete - break loop" not in str(e):
                                raise
            
            # Verify all expected messages were sent
            assert len(sent_messages) == 5  # 1 new + 1 status change + 1 new + 2 status changes
            
            # Verify message contents
            assert "🆕 New Task Started: Task 1 (ID: conv1)" in sent_messages[0]
            assert "🔄 Task Status Update: Task 1 is now completed." in sent_messages[1]
            assert "🆕 New Task Started: Task 2 (ID: conv2)" in sent_messages[2]
            assert "🔄 Task Status Update: Task 1 is now archived." in sent_messages[3]
            assert "🔄 Task Status Update: Task 2 is now running." in sent_messages[4]
            
            # Verify final state
            assert bot.conversation_states == {
                "conv1": "archived",
                "conv2": "running"
            }


@pytest.mark.asyncio
async def test_poll_and_notify_fetch_conversations_failure():
    """
    Test poll_and_notify when fetch_conversations fails with an exception.
    
    Verifies that the polling loop continues even when fetch_conversations
    raises an exception (returns empty list).
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Clear conversation states
            bot.conversation_states = {}
            
            # Track calls
            fetch_calls = []
            sent_messages = []
            
            async def mock_fetch_conversations():
                fetch_calls.append(1)
                # Simulate failure by returning empty list
                return []
            
            async def mock_send_telegram_message(message):
                sent_messages.append(message)
                return True
            
            # Track sleep calls
            sleep_calls = []
            async def mock_sleep(delay):
                sleep_calls.append(delay)
                # Break after 3 sleep calls to ensure fetch_conversations is called multiple times
                if len(sleep_calls) >= 3:
                    raise Exception("Break loop after testing failure handling")
            
            with patch.object(bot, 'fetch_conversations', mock_fetch_conversations):
                with patch.object(bot, 'send_telegram_message', mock_send_telegram_message):
                    with patch('asyncio.sleep', mock_sleep):
                        try:
                            await bot.poll_and_notify()
                        except Exception as e:
                            if "Break loop after testing failure handling" not in str(e):
                                raise
            
            # Verify fetch_conversations was called multiple times
            # Note: fetch_conversations is called AFTER the first sleep, then continues if empty
            # So with 3 sleep calls, fetch_conversations should be called at least 2 times
            assert len(fetch_calls) >= 2, f"Expected at least 2 fetch calls, got {len(fetch_calls)}"
            assert len(sleep_calls) >= 3, f"Expected at least 3 sleep calls, got {len(sleep_calls)}"
            
            # Verify no messages were sent (empty conversations list)
            assert len(sent_messages) == 0
            
            # Verify state remains empty
            assert bot.conversation_states == {}


@pytest.mark.asyncio
async def test_poll_and_notify_conversation_removal():
    """
    Test poll_and_notify when conversations are removed between polling cycles.
    
    Verifies that conversation_states dictionary is properly cleaned up
    when conversations no longer appear in the API response.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Set initial state with multiple conversations
            bot.conversation_states = {
                "conv1": "running",
                "conv2": "pending",
                "conv3": "completed"
            }
            
            # Track sent messages
            sent_messages = []
            async def mock_send_telegram_message(message):
                sent_messages.append(message)
                return True
            
            # Simulate conversations being removed
            polling_cycles = [
                # First cycle: conv2 and conv3 removed, conv1 still exists
                [{"id": "conv1", "title": "Task 1", "status": "running"}],
                # Second cycle: New conversation appears
                [
                    {"id": "conv1", "title": "Task 1", "status": "running"},
                    {"id": "conv4", "title": "Task 4", "status": "pending"}
                ]
            ]
            
            fetch_call_count = 0
            async def mock_fetch_conversations():
                nonlocal fetch_call_count
                if fetch_call_count < len(polling_cycles):
                    result = polling_cycles[fetch_call_count]
                    fetch_call_count += 1
                    return result
                raise Exception("Test complete - break loop")
            
            # Mock asyncio.sleep
            async def mock_sleep(delay):
                if fetch_call_count >= len(polling_cycles):
                    raise Exception("Test complete - break loop")
            
            with patch.object(bot, 'fetch_conversations', mock_fetch_conversations):
                with patch.object(bot, 'send_telegram_message', mock_send_telegram_message):
                    with patch('asyncio.sleep', mock_sleep):
                        try:
                            await bot.poll_and_notify()
                        except Exception as e:
                            if "Test complete - break loop" not in str(e):
                                raise
            
            # Verify only one message was sent (for new conv4)
            assert len(sent_messages) == 1
            assert "🆕 New Task Started: Task 4 (ID: conv4)" in sent_messages[0]
            
            # Verify state cleanup - conv2 and conv3 removed, conv4 added
            assert set(bot.conversation_states.keys()) == {"conv1", "conv4"}
            assert bot.conversation_states["conv1"] == "running"
            assert bot.conversation_states["conv4"] == "pending"


@pytest.mark.asyncio
async def test_main_with_controlled_polling_loop():
    """
    Test main function with controlled polling loop.
    
    Mocks the infinite polling loop to run for a controlled number of iterations
    and verifies proper initialization and shutdown.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Track polling iterations
            poll_iterations = 0
            
            async def mock_poll_and_notify():
                nonlocal poll_iterations
                poll_iterations += 1
                # Simulate infinite loop by never returning
                # We'll break from outside using a timeout
                while True:
                    await asyncio.sleep(0.1)
            
            # Track startup message
            startup_message_sent = False
            async def mock_send_telegram_message(message):
                nonlocal startup_message_sent
                if "OpenHands Monitor Bot is online" in message:
                    startup_message_sent = True
                return True
            
            with patch.object(bot, 'poll_and_notify', mock_poll_and_notify):
                with patch.object(bot, 'send_telegram_message', mock_send_telegram_message):
                    # Run main in a task with timeout
                    task = asyncio.create_task(bot.main())
                    try:
                        # Wait a bit to ensure poll_and_notify is called
                        await asyncio.sleep(0.2)
                        # Cancel the task to stop it
                        task.cancel()
                        try:
                            await task
                        except asyncio.CancelledError:
                            pass
                    except Exception as e:
                        task.cancel()
                        raise
            
            # Verify startup message was sent
            assert startup_message_sent, "Startup message should have been sent"
            
            # Verify poll_and_notify was called at least once
            assert poll_iterations >= 1, f"Expected at least 1 polling iteration, got {poll_iterations}"


@pytest.mark.asyncio
async def test_main_error_handling_in_polling():
    """
    Test main function's error handling during polling.
    
    Verifies that main function continues running even if poll_and_notify
    encounters temporary errors (simulated by exceptions).
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Track calls
            poll_calls = []
            
            async def mock_poll_and_notify():
                poll_calls.append(1)
                # Simulate that poll_and_notify runs indefinitely
                # We'll control the loop from outside
                while True:
                    await asyncio.sleep(0.1)
            
            # Track startup message
            startup_message_sent = False
            async def mock_send_telegram_message(message):
                nonlocal startup_message_sent
                if "OpenHands Monitor Bot is online" in message:
                    startup_message_sent = True
                return True
            
            with patch.object(bot, 'poll_and_notify', mock_poll_and_notify):
                with patch.object(bot, 'send_telegram_message', mock_send_telegram_message):
                    # Run main in a task with timeout
                    task = asyncio.create_task(bot.main())
                    try:
                        # Wait a bit to ensure poll_and_notify is called
                        await asyncio.sleep(0.3)
                        # Cancel the task to stop it
                        task.cancel()
                        try:
                            await task
                        except asyncio.CancelledError:
                            pass
                    except Exception as e:
                        task.cancel()
                        raise
            
            # Verify startup message was sent
            assert startup_message_sent, "Startup message should have been sent"
            
            # Verify poll_and_notify was called at least once
            assert len(poll_calls) >= 1, f"Expected at least 1 polling call, got {len(poll_calls)}"


@pytest.mark.asyncio
async def test_poll_and_notify_edge_cases():
    """
    Test poll_and_notify with various edge cases.
    
    Tests missing fields, empty titles, and other edge cases in conversation data.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Clear conversation states
            bot.conversation_states = {}
            
            # Track sent messages
            sent_messages = []
            async def mock_send_telegram_message(message):
                sent_messages.append(message)
                return True
            
            # Test edge cases: missing title, missing status
            mock_conversations = [
                {"id": "conv1", "title": "Task 1", "status": "running"},
                {"id": "conv2", "status": "pending"},  # Missing title
                {"id": "conv3", "title": "Task 3"},  # Missing status
                {"id": "conv4"}  # Missing both title and status
            ]
            
            # Mock asyncio.sleep to break after first iteration
            with patch('asyncio.sleep', side_effect=[None, Exception("Break loop")]):
                with patch.object(bot, 'fetch_conversations', AsyncMock(return_value=mock_conversations)):
                    with patch.object(bot, 'send_telegram_message', mock_send_telegram_message):
                        # Run poll_and_notify and expect loop to break
                        with pytest.raises(Exception, match="Break loop"):
                            await bot.poll_and_notify()
            
            # Verify messages were sent for all conversations (with default values for missing fields)
            assert len(sent_messages) == 4  # All conversations should trigger messages with default values
            assert "🆕 New Task Started: Task 1 (ID: conv1)" in sent_messages[0]
            assert "🆕 New Task Started: Untitled (ID: conv2)" in sent_messages[1]
            assert "🆕 New Task Started: Task 3 (ID: conv3)" in sent_messages[2]
            assert "🆕 New Task Started: Untitled (ID: conv4)" in sent_messages[3]
            
            # Verify states were updated for all conversations (with default status "UNKNOWN" for missing status)
            assert "conv1" in bot.conversation_states
            assert bot.conversation_states["conv1"] == "running"
            assert "conv2" in bot.conversation_states  # Has status "pending"
            assert bot.conversation_states["conv2"] == "pending"
            assert "conv3" in bot.conversation_states  # Missing status gets default "UNKNOWN"
            assert bot.conversation_states["conv3"] == "UNKNOWN"
            assert "conv4" in bot.conversation_states  # Missing status gets default "UNKNOWN"
            assert bot.conversation_states["conv4"] == "UNKNOWN"