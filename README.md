# OpenHands Monitor Bot

## Project Description

The OpenHands Monitor Bot is a Telegram bot designed to monitor OpenHands platform tasks and send real-time notifications about task status changes. It continuously polls the OpenHands API for conversation/task updates and alerts users about:

- **New tasks** being created
- **Status changes** (e.g., from "running" to "completed")
- **Task completions**

This bot helps teams stay informed about their OpenHands tasks without needing to constantly check the platform manually.

## Installation

### Prerequisites

- **Python 3.8 or higher**
- **Telegram Bot Token** (obtain from [@BotFather](https://t.me/botfather))
- **Telegram Chat ID** (use @userinfobot to find your chat ID)
- **OpenHands API access**

### Step 1: Clone the Repository

```bash
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your configuration:
   ```bash
   nano .env  # or use your preferred text editor
   ```

3. Set the required environment variables (see Configuration section below for details):
   - `TELEGRAM_TOKEN` - Your Telegram bot token (required)
   - `CHAT_ID` - Your Telegram chat ID (required)
   - `OPENHANDS_API_URL` - URL of your OpenHands API (optional, defaults to `http://host.docker.internal:3000`)
   - `POLL_INTERVAL` - Polling interval in seconds (optional, defaults to 5)

## Usage

To start the OpenHands Monitor Bot, run:

```bash
python bot.py
```

### What Happens When You Run the Bot

1. **Configuration validation**: The bot checks that all required environment variables are set
2. **Startup notification**: Sends "🤖 OpenHands Monitor Bot is online and starting to poll." to your Telegram chat
3. **Polling begins**: Starts monitoring the OpenHands API at the configured interval
4. **Notifications**: Sends alerts for:
   - New tasks: `🆕 New Task Started: {title} (ID: {conv_id})`
   - Status changes: `🔄 Task Status Update: {title} is now {status}.`

## Configuration

The bot is configured through environment variables. Create a `.env` file in the project root with the following variables:

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| **`TELEGRAM_TOKEN`** | Telegram Bot API token for authentication. Obtain from [@BotFather](https://t.me/botfather) | `TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| **`CHAT_ID`** | Telegram chat ID where notifications will be sent. Use @userinfobot to find your chat ID. | `CHAT_ID=987654321` |

### Optional Environment Variables

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| **`OPENHANDS_API_URL`** | `http://host.docker.internal:3000` | Base URL for the OpenHands API. | `OPENHANDS_API_URL=http://localhost:3000` |
| **`POLL_INTERVAL`** | `5` | Polling interval in seconds between checks for conversation updates. | `POLL_INTERVAL=10` |

### Example `.env` File

```env
# Required variables
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
CHAT_ID=987654321

# Optional variables
OPENHANDS_API_URL=http://localhost:3000
POLL_INTERVAL=5
```



