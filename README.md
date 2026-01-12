# OpenHands Monitor Bot

## Project Title & Description

The OpenHands Monitor Bot is a Telegram bot that monitors OpenHands platform tasks and sends real-time notifications about task status changes. It continuously polls the OpenHands API for conversation/task updates and alerts users about new tasks, status changes, and task completions via Telegram messages.

## Table of Contents
- [Project Title & Description](#project-title--description)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Features](#features)
- [Architecture](#architecture)
- [Development](#development)
- [Testing](#testing)
- [License](#license)

## Features

- **Real-time Monitoring**: Continuously polls OpenHands API for task updates
- **Status Change Detection**: Identifies when task status changes (e.g., from "running" to "completed")
- **Telegram Notifications**: Sends instant alerts to configured Telegram chat
- **Retry Logic**: Implements automatic retry for failed Telegram API calls
- **State Tracking**: Maintains conversation state to detect changes efficiently
- **Error Handling**: Comprehensive error handling and logging

## Installation

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

Copy the `.env.example` file to `.env` and update it with the necessary environment variables:

```bash
cp .env.example .env
```

Edit the `.env` file to set the required environment variables:

```bash
TELEGRAM_TOKEN=your_telegram_bot_token_here
CHAT_ID=your_telegram_chat_id_here
OPENHANDS_API_URL=http://localhost:3000
```

## Usage

The command to run the bot:

```bash
python bot.py
```

## Configuration

A list of all required environment variables:

- **TELEGRAM_TOKEN**: Telegram Bot API token for authentication. Obtain this token by creating a bot with [@BotFather](https://t.me/botfather) on Telegram.
- **CHAT_ID**: Telegram chat ID where notifications will be sent. Can be a user ID, group ID, or channel ID.
- **OPENHANDS_API_URL**: OpenHands API base URL. Defaults to `http://host.docker.internal:3000` if not set.

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

