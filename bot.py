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

async def send_telegram_message(message: str) -> None:
    """
    Sends a message to the configured Telegram chat.

    This function uses the global Telegram Bot instance to send a message to the
    chat ID specified in the CHAT_ID environment variable. It handles Telegram
    API errors gracefully and logs any failures.

    Args:
        message (str): The message content to send. Should be a plain text string.

    Returns:
        None: This function does not return a value.

    Raises:
        RuntimeError: If TELEGRAM_TOKEN or CHAT_ID environment variables are not set.
        telegram.error.TelegramError: If there's an error with the Telegram API
            (handled internally and logged).

    Note:
        The function uses the global `bot` instance initialized with TELEGRAM_TOKEN.
        Ensure TELEGRAM_TOKEN and CHAT_ID environment variables are set before calling.
    """
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except TelegramError as e:
        logger.error(f"Failed to send Telegram message: {e}")

async def fetch_conversations() -> list[dict]:
    """
    Fetches conversations from the OpenHands API.

    This function makes an asynchronous HTTP GET request to the OpenHands API
    endpoint to retrieve the current list of conversations/tasks. It handles
    various HTTP errors and network issues gracefully, returning an empty list
    on failure.

    Returns:
        list[dict]: A list of conversation objects, where each object contains
            conversation metadata (id, title, status, etc.). Returns an empty
            list if the request fails or no conversations are available.

    Raises:
        httpx.HTTPStatusError: If the API returns an HTTP error status (4xx, 5xx).
            Handled internally and logged.
        httpx.RequestError: If there's a network error or connection issue.
            Handled internally and logged.
        ValueError: If the response contains invalid JSON. Handled internally
            and logged.

    Note:
        The API URL is configured via the OPENHANDS_API_URL environment variable.
        The function uses httpx.AsyncClient for asynchronous HTTP requests.
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
    the OpenHands API and comparing them with the previous state. It sends
    Telegram notifications for:
    1. New conversations (tasks) that appear
    2. Status changes in existing conversations
    3. Automatically cleans up conversations that no longer exist
    
    The polling interval is controlled by the POLL_INTERVAL environment variable.

    Returns:
        None: This function runs indefinitely and does not return.

    Raises:
        RuntimeError: If required environment variables are not set (indirectly
            through called functions).
        Exception: Any unhandled exceptions from called functions will propagate
            and stop the polling loop.

    Note:
        This function maintains global state in `conversation_states` dictionary
        to track conversation statuses between polling cycles.
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
    3. Starts the main polling loop to monitor conversation changes
    
    Returns:
        None: This function runs the bot indefinitely until interrupted.

    Raises:
        ValueError: If TELEGRAM_TOKEN or CHAT_ID environment variables are not set.
        KeyboardInterrupt: When the user interrupts the program (Ctrl+C).
        SystemExit: When the program is terminated.
        Exception: Any unhandled exceptions from the polling loop.

    Note:
        The function uses asyncio.run() to manage the asynchronous event loop.
        Ensure all required environment variables are set before running.
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
