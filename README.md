# OpenHands Monitor Bot

## Project Description

The OpenHands Monitor Bot is a Telegram bot designed to monitor OpenHands platform tasks and send real-time notifications about task status changes. It continuously polls the OpenHands API for conversation/task updates and alerts users about:

- **New tasks** being created
- **Status changes** (e.g., from "running" to "completed")
- **Task completions**

This bot helps teams stay informed about their OpenHands tasks without needing to constantly check the platform manually.

### Key Features
- **Real-time monitoring**: Continuously polls the OpenHands API for task updates
- **Telegram notifications**: Sends instant alerts to configured Telegram chat
- **Status tracking**: Maintains state to detect changes between polling cycles
- **Error handling**: Gracefully handles API errors and network issues
- **Configurable polling**: Adjustable interval for checking updates

## Installation

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot
```

### Step 2: Install Dependencies

Install all required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root with the required environment variables:

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file** with your configuration (see Configuration section below for details):
   - `TELEGRAM_TOKEN` - Your Telegram bot token (required)
   - `CHAT_ID` - Your Telegram chat ID (required)
   - `OPENHANDS_API_URL` - URL of your OpenHands API (optional, defaults to `http://host.docker.internal:3000`)

## Usage

To start the OpenHands Monitor Bot, run:

```bash
python bot.py
```

The bot will:
1. Validate that all required environment variables are set
2. Send a startup notification to your Telegram chat
3. Begin polling the OpenHands API at the configured interval
4. Send notifications for new tasks and status changes

## Configuration

The bot requires the following environment variables to be set in a `.env` file:

### Required Environment Variables

- **`TELEGRAM_TOKEN`**: Your Telegram Bot API token (obtain from [@BotFather](https://t.me/botfather))
- **`CHAT_ID`**: Telegram chat ID where notifications will be sent

### Optional Environment Variables

- **`OPENHANDS_API_URL`**: Base URL for the OpenHands API (default: `http://host.docker.internal:3000`)
- **`POLL_INTERVAL`**: Polling interval in seconds (default: `5`)

### Example `.env` File

```env
# Required variables
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
CHAT_ID=987654321

# Optional variables
OPENHANDS_API_URL=http://localhost:3000
POLL_INTERVAL=5
```

**Note**: The task instructions mention `TELEGRAM_BOT_TOKEN` and `OPEN_HANDS_API_URL`, but the actual code uses `TELEGRAM_TOKEN` and `OPENHANDS_API_URL`. Use the variable names shown above for proper functionality.



