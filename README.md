# OpenHands Monitor Bot 🤖

## Project Description

The OpenHands Monitor Bot is a Telegram bot designed to monitor OpenHands platform tasks and send real-time notifications about task status changes. It continuously polls the OpenHands API for conversation/task updates and alerts users about:

- **New tasks** being created
- **Status changes** (e.g., from "running" to "completed")
- **Task completions**

This bot helps teams stay informed about their OpenHands tasks without needing to constantly check the platform manually.

### Key Features
- **Real-time Monitoring**: Continuously polls OpenHands API for task updates
- **Telegram Notifications**: Sends instant alerts to configured Telegram chat
- **Status Tracking**: Maintains state of conversations to detect changes
- **Configurable Polling**: Adjustable interval between API checks
- **Error Handling**: Robust error handling with comprehensive logging
- **Docker Support**: Easy deployment using Docker containers

## Installation

### Prerequisites

Before installing the OpenHands Monitor Bot, ensure you have the following:

- **Python 3.8 or higher** (check with `python3 --version`)
- **pip** package manager (usually comes with Python)
- **Git** for cloning the repository
- **Telegram Bot Token** (obtain from [@BotFather](https://t.me/botfather))
- **Telegram Chat ID** (use @userinfobot to find your chat ID)
- **OpenHands API access** (running instance of OpenHands platform)

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

**Note**: It's recommended to use a virtual environment to avoid conflicts with system packages:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

The bot uses environment variables for configuration. Follow these steps:

1. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file** with your configuration:
   ```bash
   nano .env  # or use your preferred text editor (vim, code, etc.)
   ```

3. **Set the required environment variables** (see Configuration section below for details):
   - `TELEGRAM_TOKEN` - Your Telegram bot token (required)
   - `CHAT_ID` - Your Telegram chat ID (required)
   - `OPENHANDS_API_URL` - URL of your OpenHands API (optional, defaults to `http://host.docker.internal:3000`)
   - `POLL_INTERVAL` - Polling interval in seconds (optional, defaults to 5)

## Usage

### Running the Bot

To start the OpenHands Monitor Bot, run:

```bash
python bot.py
```

### What Happens When You Run the Bot

1. **Configuration Validation**: The bot checks that all required environment variables (`TELEGRAM_TOKEN` and `CHAT_ID`) are properly set
2. **Startup Notification**: Sends "🤖 OpenHands Monitor Bot is online and starting to poll." to your configured Telegram chat
3. **Polling Loop Begins**: Starts monitoring the OpenHands API at the configured interval (default: 5 seconds)
4. **Notifications**: Sends real-time alerts for:
   - **New tasks**: `🆕 New Task Started: {title} (ID: {conv_id})`
   - **Status changes**: `🔄 Task Status Update: {title} is now {status}.`

### Running with Docker

If you prefer to run the bot in a Docker container:

```bash
# Build the Docker image
docker build -t openhands-monitor-bot .

# Run the container
docker run --env-file .env openhands-monitor-bot
```

Or using Docker Compose:

```bash
docker-compose up
```

### Stopping the Bot

To stop the bot, press `Ctrl+C` in the terminal where it's running. The bot will gracefully shut down and log "Bot shutting down."

## Configuration

The OpenHands Monitor Bot is configured through environment variables. Create a `.env` file in the project root directory with the following variables:

### Required Environment Variables

These variables must be set for the bot to function properly:

| Variable | Type | Description | How to Obtain | Example |
|----------|------|-------------|---------------|---------|
| **`TELEGRAM_TOKEN`** | `str` | Telegram Bot API token for authentication. This token authorizes the bot to send messages through the Telegram API. | 1. Open Telegram and search for [@BotFather](https://t.me/botfather)<br>2. Send `/newbot` command<br>3. Follow the prompts to create a new bot<br>4. Copy the token provided by BotFather | `TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| **`CHAT_ID`** | `str` | Telegram chat ID where notifications will be sent. This identifies the specific chat or user that will receive notifications. | 1. Open Telegram and search for [@userinfobot](https://t.me/userinfobot)<br>2. Start a chat with the bot<br>3. Send `/start` command<br>4. The bot will reply with your chat ID | `CHAT_ID=987654321` |

### Optional Environment Variables

These variables have default values but can be customized:

| Variable | Type | Default | Description | Example |
|----------|------|---------|-------------|---------|
| **`OPENHANDS_API_URL`** | `str` | `http://host.docker.internal:3000` | Base URL for the OpenHands API. This is the endpoint where the bot will fetch conversation data. | `OPENHANDS_API_URL=http://localhost:3000`<br>`OPENHANDS_API_URL=https://api.openhands.example.com` |
| **`POLL_INTERVAL`** | `int` | `5` | Polling interval in seconds between checks for conversation updates. Lower values provide more real-time updates but increase API load. Higher values reduce load but may delay notifications. | `POLL_INTERVAL=10`<br>`POLL_INTERVAL=30` |

### Example `.env` File

```env
# OpenHands Monitor Bot Configuration
# ===================================

# Required variables - MUST be set for the bot to work
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
CHAT_ID=987654321

# Optional variables - can be customized or left as defaults
OPENHANDS_API_URL=http://localhost:3000
POLL_INTERVAL=5
```

### Environment Variable Notes

1. **Security**: Never commit your `.env` file to version control. It contains sensitive credentials.
2. **Validation**: The bot validates all required environment variables on startup and will exit with an error if any are missing.
3. **Docker**: When running in Docker, pass the `.env` file using the `--env-file` flag.
4. **Development**: For development, you can set environment variables directly in your shell:
   ```bash
   export TELEGRAM_TOKEN="your_token_here"
   export CHAT_ID="your_chat_id_here"
   ```

## Troubleshooting

### Common Issues and Solutions

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| **"TELEGRAM_TOKEN and CHAT_ID environment variables must be set."** | Missing or incorrect environment variables | 1. Check that `.env` file exists in project root<br>2. Verify both `TELEGRAM_TOKEN` and `CHAT_ID` are set<br>3. Ensure no typos in variable names |
| **"Failed to send Telegram message"** | Invalid Telegram token or chat ID | 1. Verify token with BotFather<br>2. Confirm chat ID with @userinfobot<br>3. Check internet connection |
| **No notifications received** | OpenHands API not accessible | 1. Verify OpenHands is running<br>2. Check `OPENHANDS_API_URL` points to correct address<br>3. Ensure API endpoint `/api/conversations` is accessible |
| **Bot stops unexpectedly** | Network issues or API errors | 1. Check logs for specific error messages<br>2. Verify network connectivity<br>3. Ensure OpenHands API is responding |

### Checking Logs

The bot outputs logs to the console. Common log messages include:
- `INFO: Starting polling loop...` - Bot has started successfully
- `ERROR: Failed to send Telegram message: ...` - Telegram API error
- `ERROR: HTTP error fetching conversations: ...` - OpenHands API error
- `INFO: Bot shutting down.` - Normal shutdown when Ctrl+C is pressed

## Development

### Running Tests

The project includes comprehensive tests. To run the test suite:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=bot --cov-report=html

# Run specific test file
pytest tests/test_bot.py
```

### Code Style

The project follows PEP8 standards. To check code style:

```bash
# Install development dependencies
pip install flake8 black

# Check code style
flake8 bot.py tests/

# Auto-format code
black bot.py tests/
```

### Project Structure

```
openhands-monitor-bot/
├── bot.py              # Main bot module
├── map_maker.py        # Dictionary utility module
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment configuration
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── tests/              # Test suite
│   ├── test_bot.py     # Bot tests
│   └── conftest.py     # Test configuration
└── README.md           # This documentation file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure they pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

