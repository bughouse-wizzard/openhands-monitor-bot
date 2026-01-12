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

    Args:
        message (str): The message content to send to the Telegram chat.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
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

    Returns:
        list[dict]: A list of conversation objects.
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
    notifications about new conversations and status changes.
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
    
    Validates environment variables and starts the polling loop.
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
