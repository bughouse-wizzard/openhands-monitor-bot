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

    This function uses the `tenacity` library to automatically retry failed
    Telegram API calls up to 3 times with 2-second intervals between attempts.

    Args:
        message (str): The message content to send to the Telegram chat.

    Returns:
        bool: True if the message was sent successfully, False otherwise.

    Raises:
        telegram.error.TelegramError: If all retry attempts fail to send the message.
    """
    await bot.send_message(chat_id=CHAT_ID, text=message)
    return True

async def fetch_conversations() -> list[dict] | None:
    """
    Fetches all conversations from the OpenHands API.

    Makes an asynchronous HTTP GET request to the OpenHands API endpoint
    to retrieve the current list of conversations/tasks. Handles various
    error conditions including HTTP errors, network issues, and JSON parsing
    failures.

    Returns:
        list[dict] | None: A list of conversation dictionaries if successful,
            None if an error occurs. Each dictionary contains conversation
            metadata including 'id', 'title', and 'status' fields.

    Raises:
        httpx.HTTPStatusError: If the API returns an HTTP error status (4xx, 5xx).
        httpx.RequestError: If there is a network or connection error.
        ValueError: If the response cannot be parsed as valid JSON.
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

    This function runs indefinitely, periodically fetching conversations from
    the OpenHands API and comparing them with the previous state. It detects:
    - New conversations: Sends notification when a new task appears
    - Status changes: Sends notification when a task's status changes
    - Removed conversations: Cleans up internal state when tasks are removed

    The polling interval is controlled by the POLL_INTERVAL constant (default: 5 seconds).

    Note:
        This function modifies the global `conversation_states` dictionary to
        track conversation states between polling cycles.
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

    This is the main entry point for the bot application. It performs the following:
    1. Validates that required environment variables are set
    2. Sends a startup notification to the configured Telegram chat
    3. Enters the main polling loop to monitor conversation changes

    Environment Variables:
        TELEGRAM_TOKEN (str): Telegram Bot API token for authentication.
        CHAT_ID (str): Telegram chat ID where notifications will be sent.
        OPENHANDS_API_URL (str, optional): OpenHands API base URL.
            Defaults to 'http://host.docker.internal:3000'.

    Raises:
        ValueError: If TELEGRAM_TOKEN or CHAT_ID environment variables are not set.
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
