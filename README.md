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

### 1. Clone the Repository

```bash
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

The bot requires environment variables to be set. The easiest way is to use a `.env` file:

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and set the following variables:
   - `TELEGRAM_TOKEN`: Your Telegram bot token
   - `CHAT_ID`: Your Telegram chat ID
   - `OPENHANDS_API_URL`: OpenHands API base URL (default: `http://localhost:3000`)

## Usage

### Running the Bot

After completing the installation and configuration steps, run the bot with:

```bash
python bot.py
```

The bot will start polling the OpenHands API and send Telegram notifications when conversation status changes are detected.

## Configuration

The bot requires the following environment variables to be set:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_TOKEN` | Telegram Bot API token for authentication | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `CHAT_ID` | Telegram chat ID where notifications will be sent | `123456789` |
| `OPENHANDS_API_URL` | OpenHands API base URL (optional, has default) | `http://localhost:3000` |

### Variable Details

- **TELEGRAM_TOKEN**: Obtain this token by creating a bot with [@BotFather](https://t.me/botfather) on Telegram
- **CHAT_ID**: Your Telegram chat ID (can be a user ID, group ID, or channel ID)
- **OPENHANDS_API_URL**: Base URL for the OpenHands API (defaults to `http://host.docker.internal:3000` if not set)

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

