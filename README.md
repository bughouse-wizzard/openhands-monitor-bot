# OpenHands Monitor Bot

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

Telegram monitoring bot for tracking tasks in the OpenHands platform with notification delivery to Telegram.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [License](#license)

## Overview

OpenHands Monitor Bot is a monitoring system that tracks changes in OpenHands platform tasks and sends notifications to Telegram about:
- Creation of new tasks
- Changes in status of existing tasks
- Task completion

## Features

- **Automatic Monitoring**: Continuous polling of OpenHands API to track changes
- **Telegram Notifications**: Instant alerts about events
- **Flexible Configuration**: Setup through environment variables
- **Docker Containerization**: Ready-to-use image for quick deployment
- **Dictionary Module**: Additional `map_maker.py` module for working with word definitions

## Project Structure

```
openhands-monitor-bot/
├── bot.py              # Main OpenHands task monitoring module
├── map_maker.py        # Word definitions module
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker container configuration
├── docker-compose.yml # Docker Compose configuration
├── tests/             # Tests
│   ├── __init__.py
│   ├── test_bot.py
│   └── test_map_maker.py
├── README.md          # Documentation (this file)
├── LICENSE            # MIT License
└── Implementation Plan.md  # Implementation plan
```

## Installation

### Prerequisites
- Python 3.11 or higher
- Docker and Docker Compose (for containerization)
- Telegram account with a bot created via [@BotFather](https://t.me/botfather)

### Quick Start (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
export TELEGRAM_TOKEN="your_bot_token"
export CHAT_ID="your_chat_id"

# 4. Run the bot
python bot.py
```

### Getting Telegram Token and Chat ID
1. Create a bot via [@BotFather](https://t.me/botfather)
2. Add the bot to the desired chat/channel
3. Get Chat ID:
```bash
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates"
```

### Detailed Installation Methods

#### Method 1: Direct Installation with pip (all dependencies including test)
```bash
pip install -r requirements.txt
```

#### Method 2: Install only core dependencies
```bash
pip install python-telegram-bot httpx tenacity asyncio
```

#### Method 3: Installation via Docker
```bash
docker build -t openhands-monitor .
```

## Configuration

### Environment Variables

Before running, configure the following environment variables:

| Variable | Description | Required | Default Value | Example |
|----------|-------------|----------|---------------|---------|
| `TELEGRAM_TOKEN` | Your Telegram bot token | Yes | None | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `CHAT_ID` | Chat ID for sending notifications | Yes | None | `-1001234567890` |
| `OPENHANDS_API_URL` | OpenHands API URL | No | `http://host.docker.internal:3000` | `http://localhost:3000` or `http://api.openhands.example.com` |

**Note about `OPENHANDS_API_URL`:**
- **Default**: `http://host.docker.internal:3000` - for Docker containers (without `host` network mode)
- **For Docker with `network_mode: host`**: Use `http://localhost:3000`
- **For local run without Docker**: Use `http://localhost:3000`
- **For production**: Specify the full URL of your API server

### Setting Up Environment Variables

#### Option 1: Export directly in shell
```bash
export TELEGRAM_TOKEN="your_token"
export CHAT_ID="your_chat_id"
export OPENHANDS_API_URL="http://localhost:3000"
```

#### Option 2: Create `.env` file
Create a `.env` file in the project root:
```bash
TELEGRAM_TOKEN=your_token
CHAT_ID=your_chat_id
OPENHANDS_API_URL=http://localhost:3000
```

#### Option 3: Docker Compose with `.env` file
1. Create `.env` file:
```bash
TELEGRAM_TOKEN=your_token
CHAT_ID=your_chat_id
OPENHANDS_API_URL=http://localhost:3000
```

2. Run with Docker Compose:
```bash
docker-compose up -d
```

## Usage

### Running the Application

#### Method 1: Direct run
```bash
export TELEGRAM_TOKEN="your_token"
export CHAT_ID="your_chat_id"
python bot.py
```

#### Method 2: Run via Docker Compose
```bash
docker-compose up -d
```

#### Method 3: Manual Docker run
```bash
docker run -d \
  --name openhands-monitor \
  --network host \
  -e TELEGRAM_TOKEN="your_token" \
  -e CHAT_ID="your_chat_id" \
  -e OPENHANDS_API_URL="http://localhost:3000" \
  openhands-monitor
```

### Example 1: Basic monitoring setup
```bash
# Set environment variables
export TELEGRAM_TOKEN="123456:ABCdef"
export CHAT_ID="-1001234567890"

# Run the bot
python bot.py
```

**Expected output:**
```
🤖 OpenHands Monitor Bot is online and starting to poll.
Starting polling loop...
```

**Example Telegram notifications:**
- 🆕 New Task Started: "New feature development" (ID: task_123)
- 🔄 Task Status Update: "New feature development" is now IN_PROGRESS.
- 🔄 Task Status Update: "New feature development" is now COMPLETED.

### Example 2: Using the map_maker.py module
```python
from map_maker import get_definitions

# Get definitions from standard dictionary
definitions = get_definitions("apple")
print(definitions)
# Output: ['A fruit that grows on trees', 'A technology company founded by Steve Jobs']

# Using custom dictionary
custom_dict = {
    "openhands": ["Best platform for AI development"],
    "python": ["My favorite programming language"]
}
definitions = get_definitions("python", custom_dict)
print(definitions)
# Output: ['My favorite programming language']

# Word not found
definitions = get_definitions("nonexistent")
print(definitions)
# Output: []
```

### Example 3: Running with custom API URL
```bash
export TELEGRAM_TOKEN="your_token"
export CHAT_ID="your_chat_id"
export OPENHANDS_API_URL="https://api.openhands.example.com"
python bot.py
```

## Development

### Code Style & Quality
- **PEP8**: All Python code must follow PEP8 standards
- **Type Hinting**: Mandatory use of type annotations for all function arguments and return values
- **Modularity**: Break code into small, reusable functions
- **Error Handling**: Use `try-except` blocks for external calls (API, Database, Filesystem)

### Architecture
- Project is built as a Telegram bot for OpenHands monitoring
- Main file: `bot.py`
- All configuration parameters (tokens, URLs) should be loaded from environment variables

### File Descriptions

#### **bot.py** - Main monitoring module
- Asynchronous bot for monitoring OpenHands tasks
- Sends notifications to Telegram about new tasks and status changes
- Uses `asyncio` for efficient API polling
- Configured through environment variables

#### **map_maker.py** - Dictionary module
- `get_definitions()` function for retrieving word definitions
- Supports standard and custom dictionaries
- Case-insensitive search with input normalization
- Full test coverage

#### **requirements.txt** - Python dependencies
```txt
python-telegram-bot  # Telegram API integration
httpx                # Asynchronous HTTP requests
tenacity             # Retry mechanisms
asyncio              # Asynchronous programming

# Testing dependencies (optional, for development)
pytest               # Test framework
pytest-asyncio       # Async test support
pytest-cov           # Coverage integration
coverage             # Code coverage analysis
```

## Testing

### Framework
- Use **pytest** as the main testing framework

### Test Structure
- Tests should be in the `tests/` directory
- Test file names should match the module being tested: `test_bot.py`

### Requirements
1. **Mocking**: All external calls (Telegram API, OpenHands API) must be mocked using `unittest.mock` (`patch`, `MagicMock`)
   - *No real network requests in tests!*
2. **Coverage**: Aim for coverage > 80% for business logic
3. **Positive & Negative**: Test both successful scenarios (200 OK) and errors (400, 500, ConnectionError)

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_bot.py

# Run tests with verbose output
pytest -v
```

### Example Test
```python
@patch('bot.requests.get')
def test_fetch_conversations_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"id": "123", "status": "running"}]
    
    result = fetch_conversations()
    assert len(result) == 1
    assert result[0]['id'] == "123"
```

## Deployment

### Docker Deployment
```bash
# Build the image
docker build -t openhands-monitor .

# Run the container
docker run -d \
  --name openhands-monitor \
  --restart always \
  --network host \
  -e TELEGRAM_TOKEN="your_token" \
  -e CHAT_ID="your_chat_id" \
  -e OPENHANDS_API_URL="http://localhost:3000" \
  openhands-monitor
```

### Docker Compose Deployment
```yaml
# docker-compose.yml
version: '3.8'
services:
  openhands-monitor:
    build: .
    container_name: openhands-monitor
    restart: always
    network_mode: host
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - CHAT_ID=${CHAT_ID}
      - OPENHANDS_API_URL=http://localhost:3000
```

### Production Considerations
1. **Security**: Use secure methods for storing tokens and secrets
2. **Monitoring**: Set up logging and monitoring for the bot
3. **Backup**: Regular backups of configuration
4. **Updates**: Keep dependencies updated

## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

- **Repository**: [https://github.com/bughouse-wizzard/openhands-monitor-bot](https://github.com/bughouse-wizzard/openhands-monitor-bot)
- **Issues**: [https://github.com/bughouse-wizzard/openhands-monitor-bot/issues](https://github.com/bughouse-wizzard/openhands-monitor-bot/issues)

---

*Made with ❤️ for the OpenHands community*

*Documentation verified and updated: 2026-01-09*