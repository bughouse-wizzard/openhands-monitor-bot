# OpenHands Monitor Bot

## Project Description

The OpenHands Monitor Bot is a Telegram bot designed to monitor OpenHands platform tasks and send real-time notifications about task status changes. It continuously polls the OpenHands API for conversation/task updates and alerts users about:

- **New tasks** being created
- **Status changes** (e.g., from "running" to "completed")
- **Task completions**

This bot helps teams stay informed about their OpenHands tasks without needing to constantly check the platform manually.

## Features

- **Real-time monitoring**: Continuously polls the OpenHands API for updates
- **Telegram notifications**: Sends instant alerts to configured Telegram chat
- **State tracking**: Remembers previous conversation states to detect changes
- **Error handling**: Robust error handling with comprehensive logging
- **Configurable polling**: Adjustable polling interval for different needs

## Installation

### Prerequisites

- **Python 3.8 or higher** - The bot is built with Python and requires modern Python features
- **Telegram Bot Token** - Obtain from [@BotFather](https://t.me/botfather) by creating a new bot
- **Telegram Chat ID** - Your personal chat ID or group/channel ID where notifications will be sent
- **OpenHands API access** - Access to an OpenHands instance with API endpoints available
- **Git** - For cloning the repository (optional if downloading manually)

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot
```

### Step 2: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

**Alternative: Using virtual environment (recommended)**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

1. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file** with your configuration:
   ```bash
   nano .env  # or use your preferred text editor
   ```

3. **Set the required environment variables** (see Configuration section below for details):
   - `TELEGRAM_TOKEN` - Your Telegram bot token (required)
   - `CHAT_ID` - Your Telegram chat ID (required)
   - `OPENHANDS_API_URL` - URL of your OpenHands API (optional, defaults to `http://host.docker.internal:3000`)
   - `POLL_INTERVAL` - Polling interval in seconds (optional, defaults to 5)

## Usage

### Basic Usage

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

### Running in Background

To run the bot in the background (Linux/macOS):

```bash
nohup python bot.py > bot.log 2>&1 &
```

### Stopping the Bot

Press `Ctrl+C` in the terminal where the bot is running.

## Configuration

The bot is configured through environment variables. Create a `.env` file in the project root with the following variables:

### Required Environment Variables

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| **`TELEGRAM_TOKEN`** | string | Telegram Bot API token for authentication. Obtain from [@BotFather](https://t.me/botfather) | `TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| **`CHAT_ID`** | string | Telegram chat ID where notifications will be sent. Can be user ID, group ID, or channel ID. Use @userinfobot to find your chat ID. | `CHAT_ID=987654321` |

### Optional Environment Variables

| Variable | Type | Default | Description | Example |
|----------|------|---------|-------------|---------|
| **`OPENHANDS_API_URL`** | string | `http://host.docker.internal:3000` | Base URL for the OpenHands API. If not set, defaults to `http://host.docker.internal:3000`. | `OPENHANDS_API_URL=http://localhost:3000` |
| **`POLL_INTERVAL`** | int | `5` | Polling interval in seconds between checks for conversation updates. | `POLL_INTERVAL=10` |

### Polling Configuration

The polling interval can be configured either by setting the `POLL_INTERVAL` environment variable or by modifying the `POLL_INTERVAL` constant in `bot.py`. The environment variable takes precedence if set.

### Example `.env` File

```env
# Required variables
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
CHAT_ID=987654321

# Optional variables
OPENHANDS_API_URL=http://localhost:3000
POLL_INTERVAL=5
```

## Development

### Project Structure

```
openhands-monitor-bot/
├── bot.py              # Main bot implementation
├── requirements.txt    # Python dependencies
├── README.md          # This documentation
├── .env.example       # Example environment configuration
├── tests/             # Test files
└── Dockerfile         # Docker configuration
```

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows:
- **PEP 8** for Python code style
- **Google Style** docstrings for documentation
- **Type hints** for all function signatures

## Troubleshooting

### Common Issues

1. **"TELEGRAM_TOKEN and CHAT_ID environment variables must be set."**
   - Solution: Ensure your `.env` file exists and contains both variables

2. **Telegram messages not sending**
   - Check that your Telegram token is valid
   - Verify the chat ID is correct
   - Ensure the bot has been added to the chat/channel

3. **No conversations being detected**
   - Verify the `OPENHANDS_API_URL` is correct
   - Check that the OpenHands API is running and accessible
   - Review logs for HTTP errors

### Logs

The bot logs to stdout with the following format:
```
2024-01-12 10:30:00,000 - bot - INFO - Starting polling loop...
```

Check logs for error messages and debugging information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

