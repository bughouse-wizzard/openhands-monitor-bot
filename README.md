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

### Prerequisites

Before installing the OpenHands Monitor Bot, ensure you have the following:

- **Python 3.8 or higher** - The bot is built with modern Python async features
- **Telegram Bot Token** - Obtain from [@BotFather](https://t.me/botfather) on Telegram
- **Telegram Chat ID** - Use @userinfobot on Telegram to find your chat ID
- **OpenHands API access** - Access to an OpenHands instance with API endpoints
- **Git** - For cloning the repository (optional, can download ZIP instead)

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot
```

Alternatively, you can download the repository as a ZIP file from GitHub and extract it.

### Step 2: Install Dependencies

Install all required Python packages using pip:

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `python-telegram-bot` - Telegram Bot API wrapper
- `httpx` - Async HTTP client for API requests
- `tenacity` - Retry logic for handling transient failures
- `asyncio` - Async I/O framework (built-in for Python 3.8+)

**Optional development dependencies:**
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Test coverage reporting
- `coverage` - Code coverage analysis

### Step 3: Configure Environment Variables

The bot is configured through environment variables. Follow these steps:

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file** with your configuration:
   ```bash
   # Using nano (or your preferred text editor)
   nano .env
   ```

3. **Set the required environment variables** (see Configuration section below for details):
   - `TELEGRAM_TOKEN` - Your Telegram bot token (required)
   - `CHAT_ID` - Your Telegram chat ID (required)
   - `OPENHANDS_API_URL` - URL of your OpenHands API (optional, defaults to `http://host.docker.internal:3000`)
   - `POLL_INTERVAL` - Polling interval in seconds (optional, defaults to 5)

## Usage

### Starting the Bot

To start the OpenHands Monitor Bot, run:

```bash
python bot.py
```

### What Happens When You Run the Bot

When you start the bot, it performs the following sequence:

1. **Configuration validation**: The bot checks that all required environment variables (`TELEGRAM_TOKEN` and `CHAT_ID`) are properly set
2. **Startup notification**: Sends "🤖 OpenHands Monitor Bot is online and starting to poll." to your configured Telegram chat
3. **Polling begins**: Starts monitoring the OpenHands API at the configured interval (default: 5 seconds)
4. **Continuous monitoring**: The bot enters an infinite loop, periodically checking for conversation updates

### Notification Types

The bot sends the following types of notifications:

1. **New Task Started**: When a new conversation/task appears in OpenHands
   ```
   🆕 New Task Started: {title} (ID: {conv_id})
   ```

2. **Task Status Update**: When an existing task's status changes
   ```
   🔄 Task Status Update: {title} is now {status}.
   ```

### Stopping the Bot

To stop the bot, press `Ctrl+C` in the terminal where it's running. The bot will:
- Gracefully shut down the polling loop
- Log a shutdown message
- Exit cleanly

### Running in Background

For production use, you may want to run the bot in the background:

```bash
# Using nohup (simple approach)
nohup python bot.py > bot.log 2>&1 &

# Using systemd (recommended for production)
# Create a systemd service file: /etc/systemd/system/openhands-bot.service
```

### Docker Usage

If you prefer to run the bot in Docker:

```bash
# Build the Docker image
docker build -t openhands-monitor-bot .

# Run the container
docker run --env-file .env openhands-monitor-bot
```

See the `Dockerfile` and `docker-compose.yml` files for more details.

## Configuration

The OpenHands Monitor Bot is configured entirely through environment variables. This approach provides flexibility for different deployment environments (development, testing, production).

### Environment Variables Overview

Create a `.env` file in the project root directory with the following variables. You can use the provided `.env.example` file as a template.

### Required Environment Variables

These variables must be set for the bot to function:

| Variable | Type | Description | How to Obtain | Example |
|----------|------|-------------|---------------|---------|
| **`TELEGRAM_TOKEN`** | `string` | Telegram Bot API token for authentication. Used to authenticate with Telegram's Bot API. | 1. Message [@BotFather](https://t.me/botfather) on Telegram<br>2. Send `/newbot` command<br>3. Follow prompts to create a new bot<br>4. Copy the token provided | `TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| **`CHAT_ID`** | `string` | Telegram chat ID where notifications will be sent. Can be a user ID, group ID, or channel ID. | 1. Message [@userinfobot](https://t.me/userinfobot) on Telegram<br>2. Send `/start` command<br>3. Copy your "Id" from the response | `CHAT_ID=987654321` |

### Optional Environment Variables

These variables have default values but can be customized:

| Variable | Type | Default | Description | Recommended Values | Example |
|----------|------|---------|-------------|-------------------|---------|
| **`OPENHANDS_API_URL`** | `string` | `http://host.docker.internal:3000` | Base URL for the OpenHands API endpoint. The bot will append `/api/conversations` to this URL. | - Local development: `http://localhost:3000`<br>- Docker: `http://host.docker.internal:3000`<br>- Remote server: `https://api.openhands.example.com` | `OPENHANDS_API_URL=http://localhost:3000` |
| **`POLL_INTERVAL`** | `integer` | `5` | Polling interval in seconds between checks for conversation updates. Lower values provide faster notifications but increase API load. | - Development: `5-10` seconds<br>- Production: `10-30` seconds<br>- High-load: `30-60` seconds | `POLL_INTERVAL=10` |

### Example `.env` File

Here's a complete example `.env` file with all variables:

```env
# OpenHands Monitor Bot Configuration
# ====================================

# REQUIRED: Telegram Configuration
# ---------------------------------
# Get your token from @BotFather on Telegram
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Get your chat ID from @userinfobot on Telegram
CHAT_ID=987654321

# OPTIONAL: OpenHands API Configuration
# -------------------------------------
# Default: http://host.docker.internal:3000
# For local development, use: http://localhost:3000
OPENHANDS_API_URL=http://localhost:3000

# OPTIONAL: Polling Configuration
# -------------------------------
# Polling interval in seconds (default: 5)
# Adjust based on your needs and API rate limits
POLL_INTERVAL=5
```

### Configuration Validation

The bot validates configuration on startup:
1. **Required variables**: `TELEGRAM_TOKEN` and `CHAT_ID` must be set
2. **Type validation**: `POLL_INTERVAL` must be a valid integer
3. **URL validation**: `OPENHANDS_API_URL` should be a valid URL format

If validation fails, the bot will exit with an error message indicating which variable is missing or invalid.

### Environment Variable Sources

The bot reads environment variables from the following sources (in order of priority):
1. **System environment variables** (highest priority)
2. **`.env` file** in the project root directory
3. **Default values** (for optional variables only)

This allows you to override `.env` file values with system environment variables, which is useful for containerized deployments.

## Development

### Project Structure

```
openhands-monitor-bot/
├── bot.py                 # Main bot application
├── map_maker.py           # Additional utility module
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This documentation file
├── Dockerfile            # Docker container definition
├── docker-compose.yml    # Docker Compose configuration
├── tests/                # Test suite
│   ├── test_bot.py       # Main bot tests
│   ├── test_bot_focused.py # Focused bot tests
│   └── test_map_maker.py # Map maker tests
└── TECHNICAL_DOCUMENTATION.md # Technical guidelines
```

### Code Style

The project follows PEP 8 style guidelines and includes comprehensive type hints. All functions use Google-style docstrings as shown in the Technical Documentation.

### Running Tests

To run the test suite:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=bot --cov-report=html

# Run specific test file
pytest tests/test_bot.py
```

### Adding New Features

When adding new features:
1. Follow the existing code patterns and style
2. Add comprehensive type hints to all functions
3. Include Google-style docstrings with detailed descriptions
4. Write corresponding tests for new functionality
5. Update documentation as needed

## Troubleshooting

### Common Issues

#### 1. "TELEGRAM_TOKEN and CHAT_ID environment variables must be set"
**Solution**: Ensure your `.env` file exists in the project root and contains both `TELEGRAM_TOKEN` and `CHAT_ID` variables with valid values.

#### 2. "Failed to send Telegram message"
**Solution**: 
- Verify your Telegram bot token is correct
- Ensure the bot has been started with @BotFather
- Check that the chat ID is correct and the bot has permission to send messages

#### 3. "HTTP error fetching conversations"
**Solution**:
- Verify the `OPENHANDS_API_URL` is correct and accessible
- Check that the OpenHands API is running
- Ensure network connectivity between the bot and OpenHands instance

#### 4. Bot stops unexpectedly
**Solution**:
- Check the logs for error messages
- Verify all environment variables are set correctly
- Ensure the OpenHands API is consistently available

### Logging

The bot uses Python's `logging` module with the following log levels:
- **INFO**: Startup, shutdown, and normal operation messages
- **ERROR**: Failed API calls, configuration errors, and critical issues
- **DEBUG**: Detailed debugging information (enable by setting `LOG_LEVEL=DEBUG`)

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure they pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Pull Request Guidelines
- Follow the existing code style and conventions
- Include tests for new functionality
- Update documentation as needed
- Ensure all tests pass before submitting

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or feature requests:
1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing issues on GitHub
3. Open a new issue with detailed information about your problem

## Acknowledgments

- [OpenHands](https://github.com/OpenHands) - The platform being monitored
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [httpx](https://www.python-httpx.org/) - Async HTTP client

