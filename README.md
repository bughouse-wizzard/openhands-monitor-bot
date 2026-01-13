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

1. **Configuration validation**: The bot checks that all required environment variables are set
2. **Startup notification**: Sends "🤖 OpenHands Monitor Bot is online and starting to poll." to your Telegram chat
3. **Polling begins**: Starts monitoring the OpenHands API at the configured interval
4. **Notifications**: Sends alerts for:
   - New tasks: `🆕 New Task Started: {title} (ID: {conv_id})`
   - Status changes: `🔄 Task Status Update: {title} is now {status}.`

### Running in Background

For production use, you may want to run the bot as a background service:

```bash
# Using nohup (simple approach)
nohup python bot.py > bot.log 2>&1 &

# Using systemd (recommended for Linux servers)
# Create a service file at /etc/systemd/system/openhands-bot.service
```

### Docker Deployment

If you prefer containerized deployment:

```bash
# Build the Docker image
docker build -t openhands-monitor-bot .

# Run the container
docker run -d \
  --name openhands-bot \
  --env-file .env \
  openhands-monitor-bot
```

### Stopping the Bot

To stop the bot, use Ctrl+C in the terminal where it's running, or:

```bash
# If running in background with nohup
pkill -f "python bot.py"

# If running with Docker
docker stop openhands-bot
```

## Configuration

The bot is configured through environment variables. Create a `.env` file in the project root with the following variables:

### Required Environment Variables

| Variable | Description | Example | Validation |
|----------|-------------|---------|------------|
| **`TELEGRAM_TOKEN`** | Telegram Bot API token for authentication. Obtain from [@BotFather](https://t.me/botfather) | `TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` | Must be a valid Telegram Bot token format (numbers:letters) |
| **`CHAT_ID`** | Telegram chat ID where notifications will be sent. Use @userinfobot to find your chat ID. | `CHAT_ID=987654321` | Must be a numeric ID |

### Optional Environment Variables

| Variable | Default | Description | Example | Notes |
|----------|---------|-------------|---------|-------|
| **`OPENHANDS_API_URL`** | `http://host.docker.internal:3000` | Base URL for the OpenHands API. | `OPENHANDS_API_URL=http://localhost:3000` | Include protocol (http/https) and port if needed |
| **`POLL_INTERVAL`** | `5` | Polling interval in seconds between checks for conversation updates. | `POLL_INTERVAL=10` | Minimum: 1 second, Maximum: 3600 seconds (1 hour) |

### Example `.env` File

```env
# Required variables
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
CHAT_ID=987654321

# Optional variables
OPENHANDS_API_URL=http://localhost:3000
POLL_INTERVAL=5
```

### Environment Variable Validation

The bot validates environment variables on startup:
1. **TELEGRAM_TOKEN**: Must be non-empty and in the format `numbers:letters`
2. **CHAT_ID**: Must be a non-empty string that can be converted to an integer
3. **OPENHANDS_API_URL**: Must be a valid URL format (if provided)
4. **POLL_INTERVAL**: Must be a positive integer (if provided)

If validation fails, the bot will exit with an error message indicating which variable is invalid.

## Development

### Project Structure

```
openhands-monitor-bot/
├── bot.py              # Main bot application
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── tests/              # Test directory
│   └── test_bot.py     # Unit tests
└── .gitignore          # Git ignore file
```

### Code Style

The project follows Python best practices:
- **PEP 8** coding standards
- **Google-style docstrings** for all functions
- **Type hints** for function parameters and return values
- **Async/await** pattern for asynchronous operations

### Running Tests

To run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run tests with coverage report
pytest --cov=bot --cov-report=html
```

### Adding New Features

1. **Fork the repository** and create a feature branch
2. **Write tests** for new functionality
3. **Implement the feature** following existing code patterns
4. **Update documentation** including README and docstrings
5. **Run tests** to ensure nothing is broken
6. **Submit a pull request** with clear description of changes

## Troubleshooting

### Common Issues

#### 1. "TELEGRAM_TOKEN and CHAT_ID environment variables must be set."
- **Solution**: Ensure your `.env` file exists in the project root and contains valid values for both variables.

#### 2. "Failed to send Telegram message"
- **Solution**: 
  - Verify your Telegram bot token is correct
  - Ensure the bot has been started with @BotFather
  - Check that the CHAT_ID is correct and the bot has been added to the chat

#### 3. "HTTP error fetching conversations"
- **Solution**:
  - Verify the OPENHANDS_API_URL is correct and accessible
  - Check if the OpenHands API requires authentication
  - Ensure the API endpoint `/api/conversations` exists

#### 4. Bot stops unexpectedly
- **Solution**:
  - Check the logs for error messages
  - Ensure network connectivity to both Telegram API and OpenHands API
  - Consider adding error recovery logic or using process managers like systemd

### Logging

The bot uses Python's logging module with the following levels:
- **INFO**: Startup messages, polling status
- **WARNING**: Non-critical issues, retry attempts
- **ERROR**: Failed API calls, configuration errors
- **DEBUG**: Detailed debugging information (enable with `LOG_LEVEL=DEBUG`)

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines
- Write clear, concise commit messages
- Include tests for new functionality
- Update documentation as needed
- Follow existing code style and patterns

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the documentation
3. Open an issue on GitHub with detailed information about the problem

## Acknowledgments

- **OpenHands Platform** for providing the API
- **python-telegram-bot** library for Telegram integration
- **httpx** for async HTTP requests
- All contributors who help improve this project

