"""
Focused unit tests for bot.py meeting TASK 1 requirements.

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
            mock_conversations_second = [
                {"id": "1", "title": "Task 1", "status": "completed"}
            ]
            
            # Mock send_telegram_message to track calls
            mock_send = AsyncMock(return_value=True)
            
            # Create a mock for fetch_conversations that returns different values
            fetch_call_count = 0
            async def mock_fetch_conversations():
                nonlocal fetch_call_count
                fetch_call_count += 1
                if fetch_call_count == 1:
                    return mock_conversations_first
                elif fetch_call_count == 2:
                    return mock_conversations_second
                else:
                    # Return empty list to break the loop
                    return []
            
            # Mock asyncio.sleep to prevent infinite loop
            sleep_calls = []
            async def mock_sleep(delay):
                sleep_calls.append(delay)
                if len(sleep_calls) > 2:  # Stop after 2 iterations
                    raise asyncio.CancelledError()
            
            with patch.object(bot, 'fetch_conversations', side_effect=mock_fetch_conversations):
                with patch.object(bot, 'send_telegram_message', mock_send):
                    with patch('asyncio.sleep', mock_sleep):
                        # Run poll_and_notify - it should raise CancelledError after 2 iterations
                        try:
                            await bot.poll_and_notify()
                        except asyncio.CancelledError:
                            pass
                        
                        # Check calls
                        assert mock_send.call_count == 2
                        
                        # First call should be for new conversation
                        assert mock_send.call_args_list[0][0][0] == "🆕 New Task Started: Task 1 (ID: 1)"
                        
                        # Second call should be for status change
                        assert mock_send.call_args_list[1][0][0] == "🔄 Task Status Update: Task 1 is now completed."
                        
                        # Verify conversation state was updated
                        assert bot.conversation_states == {"1": "completed"}


@pytest.mark.asyncio
async def test_poll_and_notify_empty_conversations():
    """Test poll_and_notify when conversations list is empty."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Set initial state
            bot.conversation_states = {"1": "running"}
            
            # Mock fetch_conversations to return empty list
            mock_conversations = []
            
            # Mock send_telegram_message to track calls
            mock_send = AsyncMock(return_value=True)
            
            # Mock asyncio.sleep to prevent infinite loop
            sleep_calls = []
            async def mock_sleep(delay):
                sleep_calls.append(delay)
                if len(sleep_calls) > 1:  # Stop after 1 iteration
                    raise asyncio.CancelledError()
            
            with patch.object(bot, 'fetch_conversations', AsyncMock(return_value=mock_conversations)):
                with patch.object(bot, 'send_telegram_message', mock_send):
                    with patch('asyncio.sleep', mock_sleep):
                        # Run poll_and_notify - it should raise CancelledError
                        try:
                            await bot.poll_and_notify()
                        except asyncio.CancelledError:
                            pass
                        
                        # Verify send_telegram_message was NOT called
                        mock_send.assert_not_called()
                        
                        # Verify old conversation is NOT cleaned up when conversations is empty
                        # (the code should 'continue' and skip cleanup)
                        assert bot.conversation_states == {"1": "running"}


@pytest.mark.asyncio
async def test_poll_and_notify_cleanup_old_conversations():
    """Test poll_and_notify cleans up old conversations."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Set initial state with old conversation
            bot.conversation_states = {"old": "completed", "current": "running"}
            
            # Mock fetch_conversations to return only current conversation
            mock_conversations = [
                {"id": "current", "title": "Current Task", "status": "running"}
            ]
            
            # Mock send_telegram_message to track calls
            mock_send = AsyncMock(return_value=True)
            
            # Mock asyncio.sleep to prevent infinite loop
            sleep_calls = []
            async def mock_sleep(delay):
                sleep_calls.append(delay)
                if len(sleep_calls) > 1:  # Stop after 1 iteration
                    raise asyncio.CancelledError()
            
            with patch.object(bot, 'fetch_conversations', AsyncMock(return_value=mock_conversations)):
                with patch.object(bot, 'send_telegram_message', mock_send):
                    with patch('asyncio.sleep', mock_sleep):
                        # Run poll_and_notify - it should raise CancelledError
                        try:
                            await bot.poll_and_notify()
                        except asyncio.CancelledError:
                            pass
                        
                        # Verify send_telegram_message was NOT called (no changes)
                        mock_send.assert_not_called()
                        
                        # Verify old conversation is cleaned up
                        assert bot.conversation_states == {"current": "running"}


@pytest.mark.asyncio
async def test_main_function():
    """Test main function initialization."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Mock send_telegram_message and poll_and_notify
            mock_send = AsyncMock(return_value=True)
            mock_poll = AsyncMock()
            
            with patch.object(bot, 'send_telegram_message', mock_send):
                with patch.object(bot, 'poll_and_notify', mock_poll):
                    # Call main function
                    await bot.main()
                    
                    # Verify send_telegram_message was called with startup message
                    mock_send.assert_called_once_with("🤖 OpenHands Monitor Bot is online and starting to poll.")
                    
                    # Verify poll_and_notify was called
                    mock_poll.assert_called_once()


@pytest.mark.asyncio
async def test_main_missing_environment_variables():
    """Test main function raises ValueError when environment variables are missing."""
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {}, clear=True):
        with patch('telegram.Bot'):
            import bot
            
            # Call main function - should raise ValueError
            with pytest.raises(ValueError, match="TELEGRAM_TOKEN and CHAT_ID environment variables must be set."):
                await bot.main()