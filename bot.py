import os
import asyncio
import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
from telegram import Bot
from telegram.error import TelegramError

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

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def send_telegram_message(message: str) -> None:
    """
    Sends a message to the configured Telegram chat with retry logic.

    This function uses the tenacity library to automatically retry sending
    the message up to 3 times with a 2-second wait between attempts if
    Telegram API errors occur.

    Args:
        message (str): The message content to send to Telegram chat.

    Raises:
        TelegramError: If all retry attempts fail to send the message.

    Note:
        Uses global TELEGRAM_TOKEN and CHAT_ID from environment variables.
    """
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except TelegramError as e:
        print(f"Error sending Telegram message: {e}")
        raise

async def fetch_conversations() -> list[dict] | None:
    """
    Fetches all conversations from the OpenHands API.

    Makes an asynchronous HTTP GET request to the OpenHands API to retrieve
    the list of conversations. Handles various types of errors gracefully
    and returns None if the request fails.

    Returns:
        list[dict] | None: A list of conversation dictionaries if successful,
            where each dictionary contains conversation details like id, title,
            and status. Returns None if the request fails due to HTTP errors,
            network issues, or JSON parsing errors.

    Raises:
        httpx.HTTPStatusError: If the API returns an HTTP error status (4xx, 5xx).
        httpx.RequestError: If there's a network-related error.
        ValueError: If the response body cannot be parsed as JSON.

    Note:
        Uses global OPENHANDS_API_URL from environment variables.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{OPENHANDS_API_URL}/api/conversations")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error fetching conversations: {e}")
        except httpx.RequestError as e:
            print(f"Request error fetching conversations: {e}")
        except ValueError as e:
            print(f"JSON parsing error fetching conversations: {e}")
        return None

async def poll_and_notify() -> None:
    """
    The main polling loop to monitor conversation state changes.

    Continuously polls the OpenHands API at regular intervals to detect:
    1. New conversations that have started
    2. Status changes in existing conversations
    3. Conversations that have been completed or removed

    For each detected change, sends an appropriate notification to Telegram.
    Maintains an internal state dictionary to track conversation statuses
    between polling cycles.

    The function runs indefinitely until the program is terminated.

    Note:
        Uses global POLL_INTERVAL for sleep duration between polls.
        Uses global conversation_states dictionary to track conversation status.
    """
    global conversation_states
    print("Starting polling loop...")

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
    1. Validates that required environment variables are set
    2. Sends an initialization message to Telegram
    3. Starts the continuous polling loop to monitor conversation changes

    Raises:
        ValueError: If TELEGRAM_TOKEN or CHAT_ID environment variables are not set.

    Note:
        The function runs indefinitely until the program receives a termination
        signal (KeyboardInterrupt or SystemExit).
    """
    if not all([TELEGRAM_TOKEN, CHAT_ID]):
        raise ValueError("TELEGRAM_TOKEN and CHAT_ID environment variables must be set.")
    
    await send_telegram_message("🤖 OpenHands Monitor Bot is online and starting to poll.")
    await poll_and_notify()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot shutting down.")
    except ValueError as e:
        print(f"Configuration error: {e}")
