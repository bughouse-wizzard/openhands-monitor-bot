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
from unittest.mock import AsyncMock, Mock, patch, MagicMock, call

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.asyncio
async def test_send_telegram_message_success():
    """
    Test successful sending of Telegram message.
    
    Simulates a successful message sending. Uses unittest.mock.patch to mock
    the requests.post call to the Telegram API. Asserts that the mock was 
    called with the correct arguments.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test_token', 'CHAT_ID': 'test_chat_id'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            import bot
            
            # Call the function with test message
            test_message = "Test message content"
            await bot.send_telegram_message(test_message)
            
            # Verify send_message was called with correct parameters
            mock_bot_instance.send_message.assert_called_once_with(
                chat_id='test_chat_id', 
                text=test_message
            )


@pytest.mark.asyncio
async def test_send_telegram_message_failure():
    """
    Test failed message sending (e.g., due to network error).
    
    Mock requests.post to raise an exception. Assert that the function 
    handles the exception correctly (logs the error).
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test_token', 'CHAT_ID': 'test_chat_id'}):
        with patch('telegram.Bot') as mock_bot_class:
            mock_bot_instance = AsyncMock()
            mock_bot_class.return_value = mock_bot_instance
            
            # Configure mock to raise exception
            from telegram.error import TelegramError
            mock_bot_instance.send_message.side_effect = TelegramError("Network error: Connection failed")
            
            import bot
            
            # Call function and check that RetryError is raised after 3 attempts
            import tenacity
            with pytest.raises(tenacity.RetryError):
                await bot.send_telegram_message("Test message")
            
            # Verify send_message was called 3 times (due to retry decorator)
            assert mock_bot_instance.send_message.call_count == 3


@pytest.mark.asyncio
async def test_fetch_conversations_success():
    """
    Test successful retrieval of conversations from the OpenHands API.
    
    Mock the requests.get call to return a sample JSON response. Assert 
    that the function parses the response correctly and returns the 
    expected data.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {
        'TELEGRAM_TOKEN': 'test_token', 
        'CHAT_ID': 'test_chat_id',
        'OPENHANDS_API_URL': 'http://test-api:3000'
    }):
        with patch('telegram.Bot'):
            import bot
            
            # Create mock response with sample data
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = [
                {"id": "123", "title": "Test Conversation", "status": "running"},
                {"id": "456", "title": "Another Conversation", "status": "completed"}
            ]
            
            # Create mock async client
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            
            with patch('httpx.AsyncClient', return_value=mock_client):
                # Call the function
                result = await bot.fetch_conversations()
                
                # Assertions
                assert isinstance(result, list)
                assert len(result) == 2
                assert result[0]["id"] == "123"
                assert result[0]["title"] == "Test Conversation"
                assert result[0]["status"] == "running"
                assert result[1]["id"] == "456"
                assert result[1]["title"] == "Another Conversation"
                assert result[1]["status"] == "completed"
                
                # Verify get was called with correct URL
                mock_client.get.assert_called_once_with("http://test-api:3000/api/conversations")


@pytest.mark.asyncio
async def test_fetch_conversations_failure():
    """
    Test the scenario when the OpenHands API returns an error (e.g., 500 status code).
    
    Mock requests.get to return an error status code. Assert that the 
    function handles the error correctly (logs the error).
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test_token', 'CHAT_ID': 'test_chat_id'}):
        with patch('telegram.Bot'):
            import bot
            
            # Mock httpx.AsyncClient to return HTTP error
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            
            import httpx
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "HTTP error",
                request=Mock(),
                response=mock_response
            )
            mock_client.get.return_value = mock_response
            
            with patch('httpx.AsyncClient', return_value=mock_client):
                # Call the function
                result = await bot.fetch_conversations()
                
                # Verify empty list is returned on error
                assert result == []


@pytest.mark.asyncio
async def test_fetch_conversations_empty():
    """
    Test the scenario when the OpenHands API returns an empty list.
    
    Mock requests.get to return an empty JSON list. Assert that the 
    function returns an empty list.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {
        'TELEGRAM_TOKEN': 'test_token', 
        'CHAT_ID': 'test_chat_id',
        'OPENHANDS_API_URL': 'http://test-api:3000'
    }):
        with patch('telegram.Bot'):
            import bot
            
            # Create mock response with empty list
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = []
            
            # Create mock async client
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            
            with patch('httpx.AsyncClient', return_value=mock_client):
                # Call the function
                result = await bot.fetch_conversations()
                
                # Assert empty list is returned
                assert result == []
                assert isinstance(result, list)
                assert len(result) == 0


@pytest.mark.asyncio
async def test_poll_and_notify_new_conversation():
    """
    Test poll_and_notify with new conversation detection.
    
    Mock fetch_conversations to return a predefined list of conversations 
    and mock send_telegram_message to check if the correct messages are 
    sent based on changes in conversation status.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test_token', 'CHAT_ID': 'test_chat_id'}):
        with patch('telegram.Bot'):
            import bot
            
            # Reset conversation states for clean test
            bot.conversation_states = {}
            
            # Mock dependencies
            with patch('bot.fetch_conversations') as mock_fetch:
                with patch('bot.send_telegram_message') as mock_send:
                    with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
                        # Setup mock return values
                        mock_fetch.return_value = [
                            {"id": "789", "title": "New Task", "status": "running"}
                        ]
                        mock_sleep.side_effect = [None, Exception("Break loop")]
                        
                        # Call poll_and_notify and expect it to break
                        with pytest.raises(Exception, match="Break loop"):
                            await bot.poll_and_notify()
                        
                        # Verify fetch_conversations was called
                        mock_fetch.assert_called_once()
                        
                        # Verify send_telegram_message was called for new conversation
                        mock_send.assert_called_once_with("🆕 New Task Started: New Task (ID: 789)")
                        
                        # Verify conversation_states was updated
                        assert bot.conversation_states == {"789": "running"}


@pytest.mark.asyncio
async def test_poll_and_notify_status_change():
    """
    Test poll_and_notify with status change detection.
    
    Mock fetch_conversations to return conversations with changed status
    and verify that appropriate notifications are sent.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test_token', 'CHAT_ID': 'test_chat_id'}):
        with patch('telegram.Bot'):
            import bot
            
            # Setup initial conversation state
            bot.conversation_states = {"789": "running"}
            
            # Mock dependencies
            with patch('bot.fetch_conversations') as mock_fetch:
                with patch('bot.send_telegram_message') as mock_send:
                    with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
                        # Setup mock return values with status change
                        mock_fetch.return_value = [
                            {"id": "789", "title": "Existing Task", "status": "completed"}
                        ]
                        mock_sleep.side_effect = [None, Exception("Break loop")]
                        
                        # Call poll_and_notify and expect it to break
                        with pytest.raises(Exception, match="Break loop"):
                            await bot.poll_and_notify()
                        
                        # Verify fetch_conversations was called
                        mock_fetch.assert_called_once()
                        
                        # Verify send_telegram_message was called for status change
                        mock_send.assert_called_once_with("🔄 Task Status Update: Existing Task is now completed.")
                        
                        # Verify conversation_states was updated
                        assert bot.conversation_states == {"789": "completed"}


@pytest.mark.asyncio
async def test_poll_and_notify_no_changes():
    """
    Test poll_and_notify when there are no changes in conversations.
    
    Mock fetch_conversations to return same conversations and verify
    that no notifications are sent.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test_token', 'CHAT_ID': 'test_chat_id'}):
        with patch('telegram.Bot'):
            import bot
            
            # Setup initial conversation state
            bot.conversation_states = {"789": "running"}
            
            # Mock dependencies
            with patch('bot.fetch_conversations') as mock_fetch:
                with patch('bot.send_telegram_message') as mock_send:
                    with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
                        # Setup mock return values with same status
                        mock_fetch.return_value = [
                            {"id": "789", "title": "Existing Task", "status": "running"}
                        ]
                        mock_sleep.side_effect = [None, Exception("Break loop")]
                        
                        # Call poll_and_notify and expect it to break
                        with pytest.raises(Exception, match="Break loop"):
                            await bot.poll_and_notify()
                        
                        # Verify fetch_conversations was called
                        mock_fetch.assert_called_once()
                        
                        # Verify send_telegram_message was NOT called (no changes)
                        mock_send.assert_not_called()
                        
                        # Verify conversation_states remains unchanged
                        assert bot.conversation_states == {"789": "running"}


@pytest.mark.asyncio
async def test_poll_and_notify_empty_conversations():
    """
    Test poll_and_notify when fetch_conversations returns empty list.
    
    Verify that the function continues without sending notifications.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test_token', 'CHAT_ID': 'test_chat_id'}):
        with patch('telegram.Bot'):
            import bot
            
            # Setup initial conversation state
            bot.conversation_states = {"789": "running"}
            
            # Mock dependencies
            with patch('bot.fetch_conversations') as mock_fetch:
                with patch('bot.send_telegram_message') as mock_send:
                    with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
                        # Setup mock to return empty list
                        mock_fetch.return_value = []
                        mock_sleep.side_effect = [None, Exception("Break loop")]
                        
                        # Call poll_and_notify and expect it to break
                        with pytest.raises(Exception, match="Break loop"):
                            await bot.poll_and_notify()
                        
                        # Verify fetch_conversations was called
                        mock_fetch.assert_called_once()
                        
                        # Verify send_telegram_message was NOT called
                        mock_send.assert_not_called()
                        
                        # Verify conversation_states remains unchanged
                        assert bot.conversation_states == {"789": "running"}


@pytest.mark.asyncio
async def test_poll_and_notify_cleanup_old_conversations():
    """
    Test poll_and_notify cleanup of old conversations.
    
    Verify that conversations no longer in the current list are removed
    from conversation_states.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test_token', 'CHAT_ID': 'test_chat_id'}):
        with patch('telegram.Bot'):
            import bot
            
            # Setup initial conversation state with old conversations
            bot.conversation_states = {
                "old1": "running",
                "old2": "completed",
                "current": "pending"
            }
            
            # Mock dependencies
            with patch('bot.fetch_conversations') as mock_fetch:
                with patch('bot.send_telegram_message') as mock_send:
                    with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
                        # Setup mock return values with only current conversation
                        mock_fetch.return_value = [
                            {"id": "current", "title": "Current Task", "status": "pending"}
                        ]
                        mock_sleep.side_effect = [None, Exception("Break loop")]
                        
                        # Call poll_and_notify and expect it to break
                        with pytest.raises(Exception, match="Break loop"):
                            await bot.poll_and_notify()
                        
                        # Verify fetch_conversations was called
                        mock_fetch.assert_called_once()
                        
                        # Verify send_telegram_message was NOT called (no status change)
                        mock_send.assert_not_called()
                        
                        # Verify old conversations were cleaned up
                        assert "old1" not in bot.conversation_states
                        assert "old2" not in bot.conversation_states
                        assert "current" in bot.conversation_states
                        assert bot.conversation_states["current"] == "pending"


def test_module_structure():
    """
    Test that bot module has all required functions and variables.
    """
    # Remove module from cache if already imported
    if 'bot' in sys.modules:
        del sys.modules['bot']
    
    with patch.dict('os.environ', {'TELEGRAM_TOKEN': 'test', 'CHAT_ID': 'test'}):
        with patch('telegram.Bot'):
            import bot
            
            # Check required functions exist
            assert hasattr(bot, 'send_telegram_message')
            assert hasattr(bot, 'fetch_conversations')
            assert hasattr(bot, 'poll_and_notify')
            assert hasattr(bot, 'main')
            
            # Check they are callable
            assert callable(bot.send_telegram_message)
            assert callable(bot.fetch_conversations)
            assert callable(bot.poll_and_notify)
            assert callable(bot.main)
            
            # Check global variables
            assert hasattr(bot, 'conversation_states')
            assert isinstance(bot.conversation_states, dict)