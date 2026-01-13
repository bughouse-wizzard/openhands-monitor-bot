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

    Uses the global Telegram Bot instance to send a message to the chat
    specified by CHAT_ID environment variable. Handles Telegram API errors
    gracefully and logs any failures.

    Args:
        message (str): The message content to send to the Telegram chat.
            Can include emojis and standard text formatting.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
            Returns False if any TelegramError occurs during sending.

    Raises:
        telegram.error.TelegramError: If the Telegram API request fails.
            This exception is caught internally and logged, but can be
            raised if not handled by the caller.
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

    Makes an HTTP GET request to the OpenHands API endpoint to retrieve
    current conversations/tasks. Handles various error conditions including
    HTTP errors, network issues, and JSON parsing errors.

    Returns:
        list[dict]: A list of conversation objects with their metadata.
        Returns an empty list if the request fails or no conversations are found.

    Raises:
        httpx.HTTPStatusError: If the HTTP response status code indicates an error.
        httpx.RequestError: If there is a network-related error during the request.
        ValueError: If the response body cannot be parsed as valid JSON.
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
    
    Periodically fetches conversations from OpenHands API and sends
    notifications about new conversations and status changes. The function
    maintains an internal state of known conversations to detect changes
    between polling cycles.

    The loop runs indefinitely with a configurable interval (POLL_INTERVAL).
    For each polling cycle:
    1. Fetches current conversations from OpenHands API
    2. Compares with previous state to detect new conversations
    3. Sends Telegram notifications for new conversations
    4. Detects status changes in existing conversations
    5. Sends Telegram notifications for status updates
    6. Cleans up state for conversations that no longer exist

    This function never returns and runs continuously until the program
    is terminated.
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
    
    This is the main entry point of the application. It performs the following:
    1. Validates that required environment variables (TELEGRAM_TOKEN, CHAT_ID) are set
    2. Sends a startup notification to Telegram
    3. Starts the main polling loop (poll_and_notify) which runs indefinitely

    The function will raise a ValueError if required environment variables
    are missing. It handles KeyboardInterrupt and SystemExit signals for
    graceful shutdown.

    Note: This function runs the bot in an infinite loop and only returns
    when the program is terminated by external signals.
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
