import os
import asyncio
import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
from telegram import Bot
from telegram.error import TelegramError

# --- Configuration ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
OPENHANDS_API_URL = os.environ.get("OPENHANDS_API_URL", "http://host.docker.internal:3000")
POLL_INTERVAL = 5  # seconds

# --- State ---
conversation_states = {}

# --- Telegram Bot Initialization ---
bot = Bot(token=TELEGRAM_TOKEN)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def send_telegram_message(message: str):
    """Sends a message to the configured Telegram chat."""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except TelegramError as e:
        print(f"Error sending Telegram message: {e}")
        raise

async def fetch_conversations():
    """Fetches all conversations from the OpenHands API."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{OPENHANDS_API_URL}/api/conversations")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error fetching conversations: {e}")
        except httpx.RequestError as e:
            print(f"Request error fetching conversations: {e}")
        return None

async def poll_and_notify():
    """The main polling loop to check for conversation state changes."""
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

async def main():
    """Initializes and runs the bot."""
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
