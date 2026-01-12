# OpenHands Monitor Bot

A Telegram bot for monitoring OpenHands platform tasks and sending real-time notifications about task status changes.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Development](#development)
- [Testing](#testing)
- [License](#license)

## Overview

The OpenHands Monitor Bot is a real-time monitoring solution that tracks task status changes on the OpenHands platform and sends instant notifications via Telegram. It continuously polls the OpenHands API for conversation/task updates and alerts users about new tasks, status changes, and task completions.

## Features

- **Real-time Monitoring**: Continuously polls OpenHands API for task updates
- **Status Change Detection**: Identifies when task status changes (e.g., from "running" to "completed")
- **Telegram Notifications**: Sends instant alerts to configured Telegram chat
- **Retry Logic**: Implements automatic retry for failed Telegram API calls
- **State Tracking**: Maintains conversation state to detect changes efficiently
- **Error Handling**: Comprehensive error handling and logging

## Installation

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token (obtained from [@BotFather](https://t.me/botfather))
- Telegram Chat ID
- OpenHands API access

### Cloning the Repository

```bash
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Configuring the `.env` File

Create a `.env` file in the project root with the necessary environment variables:

```bash
TELEGRAM_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
OPENHANDS_API_URL=http://localhost:3000
```

## Usage

### Running the Bot

Start the monitoring bot with the following command:

```bash
python bot.py
```

### Expected Output

When the bot starts successfully, you should see:
- Log messages indicating the bot is starting
- A Telegram notification: "🤖 OpenHands Monitor Bot is online and starting to poll."
- Periodic polling logs showing API calls
- Telegram notifications for task status changes

### Stopping the Bot

Press `Ctrl+C` to gracefully stop the bot. The bot will log a shutdown message and exit.

## Configuration

### Required Environment Variables

- `TELEGRAM_TOKEN`: Your Telegram bot token
  - **Purpose**: Authentication token for the Telegram Bot API
  - **How to obtain**: Create a bot using [@BotFather](https://t.me/botfather) on Telegram
  - **Format**: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
  - **Example**: `TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

- `CHAT_ID`: Telegram chat ID for notifications
  - **Purpose**: Identifier of the chat where notifications will be sent
  - **Can be**: A user ID, group ID, or channel ID
  - **How to find**: Use @userinfobot on Telegram to find your chat ID
  - **Example**: `CHAT_ID=123456789`

- `OPENHANDS_API_URL`: OpenHands API base URL
  - **Purpose**: Base URL for the OpenHands API endpoint
  - **Default**: `http://host.docker.internal:3000`
  - **Format**: `http://localhost:3000` or `https://api.openhands.example.com`
  - **Example**: `OPENHANDS_API_URL=http://localhost:3000`

### Optional Configuration

The bot includes several configurable parameters in `bot.py`:
- `POLL_INTERVAL`: Time between API polling cycles (default: 5 seconds)
- Retry settings for Telegram API calls (3 attempts with 2-second intervals)

## Architecture

### Core Components

1. **Configuration Module**: Loads environment variables and sets up global constants
2. **Telegram Integration**: Handles message sending with retry logic using the `python-telegram-bot` library
3. **API Client**: Uses `httpx` for asynchronous HTTP requests to the OpenHands API
4. **State Manager**: Tracks conversation states to detect changes
5. **Polling Loop**: Main monitoring loop that periodically checks for updates

### Data Flow
1. Bot starts and validates configuration
2. Sends startup notification to Telegram
3. Enters infinite polling loop:
   - Fetches conversations from OpenHands API
   - Compares with previous state
   - Sends notifications for detected changes
   - Updates internal state
   - Waits for next polling cycle

## Development

### Project Structure
```
openhands-monitor-bot/
├── bot.py              # Main bot implementation
├── requirements.txt    # Python dependencies
├── README.md          # This documentation
├── tests/             # Test suite
├── .env.example       # Environment variables template
└── Dockerfile         # Containerization configuration
```

### Code Style
- Follows PEP 8 guidelines
- Uses type hints for all function signatures
- Implements comprehensive error handling
- Includes detailed logging

### Adding Features
1. Create a feature branch from `main`
2. Implement changes with appropriate tests
3. Update documentation as needed
4. Submit a pull request for review

## Testing

### Running Tests
```bash
pytest tests/
```

### Test Coverage
The project includes comprehensive tests with mocked external dependencies:
- Telegram API calls are mocked to prevent real notifications
- OpenHands API responses are simulated
- Error scenarios are tested

### Test Structure
- `test_bot.py`: Unit tests for bot functionality
- Mocked external dependencies using `unittest.mock`
- Both positive and negative test cases

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

