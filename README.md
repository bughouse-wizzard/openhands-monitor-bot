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

- **`TELEGRAM_TOKEN`** (str): Your Telegram Bot API token. Obtain this from [@BotFather](https://t.me/botfather) on Telegram.
- **`CHAT_ID`** (str): Telegram chat ID where notifications will be sent. Use @userinfobot on Telegram to find your chat ID.

### Optional Environment Variables

- **`OPENHANDS_API_URL`** (str): Base URL for the OpenHands API. Default: `http://host.docker.internal:3000`
- **`POLL_INTERVAL`** (int): Polling interval in seconds. Default: `5`

### Environment Variables Summary

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `TELEGRAM_TOKEN` | str | Yes | - | Telegram Bot API token from @BotFather |
| `CHAT_ID` | str | Yes | - | Telegram chat ID for notifications |
| `OPENHANDS_API_URL` | str | No | `http://host.docker.internal:3000` | OpenHands API base URL |
| `POLL_INTERVAL` | int | No | `5` | Polling interval in seconds |

### Example `.env` File

```env
# OpenHands Monitor Bot Configuration
# Copy this file to .env and fill in your actual values

# Required: Telegram Bot Configuration
# Get TELEGRAM_TOKEN from @BotFather on Telegram
TELEGRAM_TOKEN=your_telegram_bot_token_here

# Required: Telegram chat ID (user, group, or channel)
# Use @userinfobot on Telegram to find your chat ID
CHAT_ID=your_telegram_chat_id_here

# Optional: OpenHands API Configuration
# Default: http://host.docker.internal:3000
OPENHANDS_API_URL=http://localhost:3000

# Optional: Polling interval in seconds
# Default: 5 seconds
POLL_INTERVAL=5
```

**Note**: The task instructions mention `TELEGRAM_BOT_TOKEN` and `OPEN_HANDS_API_URL`, but the actual code uses `TELEGRAM_TOKEN` and `OPENHANDS_API_URL`. Use the variable names shown above for proper functionality.

## Development

### Project Structure

```
openhands-monitor-bot/
├── bot.py                    # Main bot application
├── README.md                 # Project documentation (this file)
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
├── tests/                   # Test files
│   └── test_bot.py          # Unit tests for bot functionality
└── openhands/               # OpenHands related modules
```

### Testing

To run the test suite:

```bash
pytest tests/
```

For test coverage report:

```bash
pytest --cov=bot tests/
```

### Code Style

The project follows PEP 8 style guidelines and uses type hints throughout. All functions include Google-style docstrings for documentation.

### Dependencies

Main dependencies are listed in `requirements.txt`:
- `python-telegram-bot`: Telegram Bot API wrapper
- `httpx`: Async HTTP client for API requests
- `tenacity`: Retry logic for API calls
- `asyncio`: Async I/O support

Development/testing dependencies:
- `pytest`: Testing framework
- `pytest-asyncio`: Async test support
- `pytest-cov`: Coverage reporting
- `coverage`: Code coverage analysis



