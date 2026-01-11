"""
OpenHands Monitor Bot - Main monitoring module.

This module provides functionality for monitoring OpenHands conversations/tasks
and sending notifications to Telegram about status changes.

Key components:
- Configuration via environment variables
- Asynchronous polling of OpenHands API
- State tracking for conversation changes
- Telegram notification system with retry logic
"""

import os
import asyncio
import logging
import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
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

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def send_telegram_message(message: str) -> bool:
    """
    Sends a message to the configured Telegram chat with retry logic.

    This function sends a message to the Telegram chat specified by the
    CHAT_ID environment variable using the bot token from TELEGRAM_TOKEN.
    It includes automatic retry logic using the tenacity library, which
    will attempt to send the message up to 3 times with a 2-second wait
    between attempts if Telegram API errors occur.

    Args:
        message (str): The message content to send to Telegram chat.
            Should be a non-empty string containing the notification text.

    Returns:
        bool: True if the message was sent successfully. If all retry
            attempts fail, a TelegramError exception is raised.

    Raises:
        TelegramError: If all retry attempts fail to send the message.

    Note:
        This function uses the global TELEGRAM_TOKEN and CHAT_ID variables
        which are loaded from environment variables at module initialization.
        Ensure these environment variables are properly set before calling
        this function.
    """
    await bot.send_message(chat_id=CHAT_ID, text=message)
    return True

async def fetch_conversations() -> list[dict] | None:
    """
    Fetches all conversations from the OpenHands API.

    Makes an asynchronous HTTP GET request to the OpenHands API endpoint
    to retrieve the current list of conversations/tasks. The function
    handles various error conditions gracefully and returns None if the
    request fails for any reason.

    The API endpoint is constructed using the OPENHANDS_API_URL environment
    variable with the path '/api/conversations' appended.

    Returns:
        list[dict] | None: A list of conversation dictionaries if successful,
            where each dictionary contains conversation details. Expected keys
            in each dictionary include:
            - 'id' (str): Unique identifier for the conversation
            - 'title' (str, optional): Title/name of the conversation
            - 'status' (str, optional): Current status of the conversation
            Returns None if the request fails due to HTTP errors, network
            issues, or JSON parsing errors.

    Raises:
        httpx.HTTPStatusError: If the API returns an HTTP error status (4xx, 5xx).
            This exception is caught internally and results in None being returned.
        httpx.RequestError: If there's a network-related error (timeout, connection
            refused, etc.). Caught internally and results in None being returned.
        ValueError: If the response body cannot be parsed as JSON. Caught internally
            and results in None being returned.

    Note:
        This function uses the global OPENHANDS_API_URL variable which is loaded
        from environment variables at module initialization. The default value is
        'http://host.docker.internal:3000' if not specified.
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
        return None

async def poll_and_notify() -> None:
    """
    The main polling loop to monitor conversation state changes.

    This function implements the core monitoring logic of the bot. It runs
    continuously in an infinite loop, performing the following actions:
    1. Sleeps for POLL_INTERVAL seconds between polling cycles
    2. Fetches current conversations from OpenHands API
    3. Compares current state with previous state to detect changes
    4. Sends notifications for detected changes to Telegram
    5. Updates internal state tracking

    Detected changes include:
    - New conversations that have started (not in previous state)
    - Status changes in existing conversations (different status)
    - Conversations that have been completed or removed (cleanup)

    The function maintains an internal dictionary (conversation_states)
    that tracks the last known status of each conversation ID between
    polling cycles.

    Returns:
        None: This function runs indefinitely until the program is
            terminated by a KeyboardInterrupt or SystemExit signal.

    Note:
        This function uses the global POLL_INTERVAL constant for sleep
        duration between polls (default: 5 seconds).
        It also uses the global conversation_states dictionary for
        tracking conversation statuses across polling cycles.
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

    This is the main entry point of the application. It performs the following
    initialization and startup sequence:
    1. Validates that required environment variables (TELEGRAM_TOKEN, CHAT_ID) are set
    2. Sends an initialization message to Telegram indicating bot startup
    3. Starts the continuous polling loop to monitor conversation changes

    The function will run indefinitely until the program receives a termination
    signal (KeyboardInterrupt or SystemExit). All application logic after
    initialization is handled by the poll_and_notify() function.

    Returns:
        None: This function runs indefinitely until program termination.

    Raises:
        ValueError: If TELEGRAM_TOKEN or CHAT_ID environment variables are not set.
            This validation occurs before any API calls are made.

    Note:
        This function should be called using asyncio.run(main()) from the
        __main__ block. It handles the top-level exception catching for
        graceful shutdown on termination signals.
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
