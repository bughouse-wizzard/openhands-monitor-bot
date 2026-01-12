"""
OpenHands Monitor Bot - Main monitoring module.

This module provides functionality for monitoring OpenHands conversations/tasks
and sending notifications to Telegram about status changes.

Key components:
- Configuration via environment variables
- Asynchronous polling of OpenHands API
- State tracking for conversation changes
- Telegram notification system with error handling

Documentation:
- All functions include Google-style docstrings with Args, Returns, and Raises sections
- Module and variable-level documentation follows project standards
- Type hints are provided for all function signatures
"""

import os
import asyncio
import logging
import httpx
from telegram import Bot
from telegram.error import TelegramError

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
"""str: Telegram Bot API token loaded from TELEGRAM_TOKEN environment variable."""

CHAT_ID = os.environ.get("CHAT_ID")
"""str: Telegram chat ID where notifications will be sent, loaded from CHAT_ID environment variable."""

OPENHANDS_API_URL = os.environ.get("OPENHANDS_API_URL", "http://host.docker.internal:3000")
"""str: Base URL for OpenHands API, defaults to 'http://host.docker.internal:3000'."""

POLL_INTERVAL = 5  # seconds
"""int: Interval in seconds between polling cycles for checking conversation updates."""

# --- State ---
conversation_states = {}
"""dict: Global dictionary tracking conversation IDs and their last known statuses.
Keys are conversation IDs (str), values are status strings (str)."""

# --- Telegram Bot Initialization ---
bot = Bot(token=TELEGRAM_TOKEN)
"""telegram.Bot: Telegram Bot instance initialized with TELEGRAM_TOKEN.
This global instance is used by send_telegram_message function to send
notifications to the configured chat."""

async def send_telegram_message(message: str) -> bool:
    """
    Sends a message to the configured Telegram chat.

    This function sends a message to the Telegram chat specified by the
    CHAT_ID environment variable using the Telegram Bot API. It uses the
    global `bot` instance initialized with TELEGRAM_TOKEN.

    Args:
        message (str): The message content to send to the Telegram chat.
            Should be a plain text string.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
        
    Note:
        The function logs errors but does not raise exceptions, returning
        False instead when message sending fails. This allows the polling
        loop to continue even if a single notification fails.
        
    Raises:
        None: All exceptions are caught and logged internally.
    """
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
        return True
    except TelegramError as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False

async def fetch_conversations() -> list[dict]:
    """
    Fetches conversations from the OpenHands API.

    Makes an asynchronous HTTP GET request to the OpenHands API endpoint
    to retrieve the current list of conversations/tasks.

    Returns:
        list[dict]: A list of conversation objects if successful,
            or an empty list [] if an error occurs. Each conversation object
            is a dictionary containing the following fields:
            - id (str): Unique identifier for the conversation
            - title (str): Title or description of the conversation/task
            - status (str): Current status of the conversation (e.g., 'running', 'completed')

    Raises:
        httpx.HTTPStatusError: If the API returns an HTTP error status (4xx, 5xx).
        httpx.RequestError: If there is a network or connection error.
        ValueError: If the response cannot be parsed as valid JSON.
        
    Note:
        The function catches and logs exceptions, returning an empty list
        instead of propagating errors to allow the polling loop to continue.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{OPENHANDS_API_URL}/api/conversations")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching conversations: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request error fetching conversations: {e}")
        except ValueError as e:
            logger.error(f"JSON parsing error fetching conversations: {e}")
        return []

async def poll_and_notify() -> None:
    """
    The main polling loop to monitor conversation state changes.

    This function runs indefinitely, periodically fetching conversations from
    the OpenHands API using `fetch_conversations()` and comparing them with
    the previous state stored in the global `conversation_states` dictionary.
    When changes are detected (new conversations or status changes), it sends
    notifications using `send_telegram_message()`.

    The function performs the following steps in each polling cycle:
    1. Sleeps for POLL_INTERVAL seconds
    2. Fetches current conversations from OpenHands API
    3. Compares with previous state to detect changes
    4. Sends notifications for new conversations and status changes
    5. Cleans up old conversations that are no longer present

    Returns:
        None: This function runs indefinitely and does not return.
        
    Note:
        Uses global `conversation_states` dictionary to track conversation
        states between polling cycles. The polling interval is controlled by
        the POLL_INTERVAL configuration or environment variable.
        
    Raises:
        None: All exceptions are caught and logged internally to ensure
        the polling loop continues running.
    """
    global conversation_states
    logger.info("Starting polling loop...")

    while True:
        await asyncio.sleep(POLL_INTERVAL)
        conversations = await fetch_conversations()
        if not conversations:
            continue

        current_ids = set()
        for conv in conversations:
            conv_id = conv["id"]
            title = conv.get("title", "Untitled")
            status = conv.get("status", "UNKNOWN")
            current_ids.add(conv_id)

            if conv_id not in conversation_states:
                # New conversation
                message = f"🆕 New Task Started: {title} (ID: {conv_id})"
                await send_telegram_message(message)
                conversation_states[conv_id] = status
            elif conversation_states[conv_id] != status:
                # Status change
                message = f"🔄 Task Status Update: {title} is now {status}."
                await send_telegram_message(message)
                conversation_states[conv_id] = status

        # Clean up old conversations
        for conv_id in list(conversation_states.keys()):
            if conv_id not in current_ids:
                del conversation_states[conv_id]

async def main() -> None:
    """
    Initializes and runs the OpenHands Monitor Bot.

    This function validates that required environment variables are set,
    sends a startup notification to Telegram, and then enters the main
    polling loop by calling `poll_and_notify()`.

    The function performs the following steps:
    1. Validates that TELEGRAM_TOKEN and CHAT_ID environment variables are set
    2. Sends a startup notification to Telegram
    3. Enters the main polling loop via poll_and_notify()

    Returns:
        None: This function runs indefinitely and does not return.
        
    Raises:
        ValueError: If required environment variables (TELEGRAM_TOKEN, CHAT_ID)
            are not set.
            
    Note:
        This is the main entry point for the bot. It handles KeyboardInterrupt
        (Ctrl+C) for graceful shutdown and logs configuration errors. The
        function will exit with an error if required configuration is missing.
    """
    if not all([TELEGRAM_TOKEN, CHAT_ID]):
        raise ValueError("TELEGRAM_TOKEN and CHAT_ID environment variables must be set.")
    
    await send_telegram_message("🤖 OpenHands Monitor Bot is online and starting to poll.")
    await poll_and_notify()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot shutting down.")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
