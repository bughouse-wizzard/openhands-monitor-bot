"""
OpenHands Monitor Bot - Main monitoring module.

This module provides functionality for monitoring OpenHands conversations/tasks
and sending notifications to Telegram about status changes.

Key components:
- Configuration via environment variables
- Asynchronous polling of OpenHands API
- State tracking for conversation changes
- Telegram notification system with error handling
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

POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", 5))  # seconds
"""int: Interval in seconds between polling cycles for checking conversation updates.
Loaded from POLL_INTERVAL environment variable, defaults to 5 if not set."""

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

    This function uses the global Telegram bot instance to send a message to the
    chat ID specified in the CHAT_ID environment variable. It handles Telegram
    API errors gracefully and logs any failures.

    Args:
        message (str): The message content to send to the Telegram chat.
            Can include emojis and formatting supported by Telegram.

    Returns:
        bool: True if the message was sent successfully, False if an error occurred.

    Raises:
        TelegramError: Propagated from the Telegram API if message sending fails.
            Note: This is caught internally and logged, but the function returns
            False instead of raising the exception.

    Examples:
        >>> await send_telegram_message("🤖 Bot is online!")
        True
        >>> await send_telegram_message("Task completed successfully!")
        True
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

    This function makes an asynchronous HTTP GET request to the OpenHands API
    endpoint configured in OPENHANDS_API_URL environment variable. It retrieves
    the list of conversations/tasks and handles various error conditions including
    HTTP errors, network issues, and JSON parsing errors.

    Returns:
        list[dict]: A list of conversation objects. Each dictionary contains:
            - id (str): Unique identifier for the conversation
            - title (str, optional): Title/name of the conversation/task
            - status (str, optional): Current status of the conversation
            - Other conversation metadata as provided by the OpenHands API
        Returns an empty list if the request fails or no conversations are available.

    Raises:
        httpx.HTTPStatusError: If the HTTP response status code indicates an error
            (4xx or 5xx). This is caught internally and logged.
        httpx.RequestError: If there's a network-related error. This is caught
            internally and logged.
        ValueError: If the response body cannot be parsed as JSON. This is caught
            internally and logged.

    Examples:
        >>> conversations = await fetch_conversations()
        >>> len(conversations)
        3
        >>> conversations[0].keys()
        dict_keys(['id', 'title', 'status'])
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
    the OpenHands API and comparing them with previously known states. It sends
    Telegram notifications when:
    1. A new conversation/task is detected
    2. An existing conversation's status changes

    The function maintains an in-memory state dictionary (conversation_states)
    to track conversation statuses between polling cycles. It also cleans up
    old conversations that are no longer present in the API response.

    The polling interval is controlled by the POLL_INTERVAL environment variable
    (default: 5 seconds).

    Note:
        This function runs in an infinite loop and should be executed as an
        asynchronous task. It will continue running until the program is
        interrupted (e.g., with Ctrl+C).

    Raises:
        Exception: Any unhandled exceptions from send_telegram_message or
            fetch_conversations will propagate up and may terminate the loop.

    Examples:
        >>> # This function is typically called from main()
        >>> await poll_and_notify()
        INFO: Starting polling loop...
        INFO: Sending notification for new task...
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

    This is the main entry point for the OpenHands Monitor Bot application.
    It performs the following steps:
    1. Validates that all required environment variables are set
    2. Sends a startup notification to Telegram
    3. Starts the main polling loop (poll_and_notify)

    The function runs indefinitely until interrupted by the user (Ctrl+C)
    or until a fatal error occurs.

    Environment Variables:
        TELEGRAM_TOKEN (str): Required. Telegram Bot API token.
        CHAT_ID (str): Required. Telegram chat ID for notifications.
        OPENHANDS_API_URL (str): Optional. OpenHands API URL.
            Default: "http://host.docker.internal:3000"
        POLL_INTERVAL (int): Optional. Polling interval in seconds.
            Default: 5

    Raises:
        ValueError: If required environment variables (TELEGRAM_TOKEN, CHAT_ID)
            are not set. This error is caught in the __main__ block and logged.
        KeyboardInterrupt: When the user presses Ctrl+C to stop the bot.
            This is caught in the __main__ block and results in graceful shutdown.
        SystemExit: When the program is terminated. Caught in __main__ block.

    Examples:
        >>> # Typically called via asyncio.run(main()) in __main__ block
        >>> await main()
        INFO: Sending startup notification...
        INFO: Starting polling loop...
        ... (bot runs until interrupted)
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
