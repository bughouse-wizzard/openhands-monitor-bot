# OpenHands Monitor Bot

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Docker Deployment](#docker-deployment)
- [Testing](#testing)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Project Overview

The **OpenHands Monitor Bot** is a sophisticated Telegram bot designed to monitor OpenHands platform tasks and send real-time notifications about task status changes. It continuously polls the OpenHands API for conversation/task updates and provides instant alerts to keep teams informed without manual monitoring.

### What It Monitors
- **New tasks** being created on the OpenHands platform
- **Status changes** (e.g., from "running" to "completed", "failed", etc.)
- **Task completions** and final status updates

### Why Use It
- **Automated Monitoring**: Eliminates the need for manual platform checking
- **Real-time Alerts**: Instant notifications via Telegram
- **Team Collaboration**: Keep entire teams informed about task progress
- **Error Detection**: Early notification of task failures or issues

## ✨ Key Features

### Core Monitoring Features
- **Real-time Monitoring**: Continuously polls the OpenHands API for task updates
- **Telegram Notifications**: Sends instant alerts to configured Telegram chat/channel
- **State Tracking**: Maintains conversation state to detect changes between polling cycles
- **Error Resilience**: Gracefully handles API errors, network issues, and retries failed operations
- **Configurable Polling**: Adjustable interval for checking updates (default: 5 seconds)

### Advanced Features
- **Dictionary Module**: Built-in word definition lookup functionality (`map_maker.py`)
- **Docker Support**: Full containerization for easy deployment
- **Comprehensive Testing**: Extensive test suite with 95%+ code coverage
- **Production Ready**: Error handling, logging, and monitoring capabilities
- **Modular Architecture**: Clean separation of concerns for easy maintenance

## 🏗️ Architecture

### System Architecture
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   OpenHands     │────▶│   Monitor Bot   │────▶│    Telegram     │
│      API        │     │   (bot.py)      │     │      API        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Conversations  │     │  State Tracking │     │  Notifications  │
│     Data        │     │   (in-memory)   │     │  to Users       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Component Architecture

#### 1. Main Monitoring Module (`bot.py`)
- **Polling Engine**: Asynchronous loop that polls OpenHands API at configurable intervals
- **State Management**: In-memory storage of conversation states for comparison
- **Notification Engine**: Sends formatted messages to Telegram
- **Error Handling**: Retry mechanisms and error recovery with tenacity library

#### 2. Dictionary Module (`map_maker.py`)
- **Dictionary Interface**: Standard dictionary with common word definitions
- **Search Function**: Case-insensitive word lookup with normalization
- **Custom Dictionary Support**: Extensible with user-provided dictionaries
- **Type Safety**: Robust handling of various input types and edge cases

### Data Flow
1. **Polling**: Bot queries OpenHands API for current conversations
2. **Comparison**: Compares current state with previous state stored in memory
3. **Detection**: Identifies new conversations and status changes
4. **Notification**: Sends appropriate messages to Telegram
5. **State Update**: Updates internal state tracking for next cycle

### Technology Stack
- **Language**: Python 3.11+
- **Async Framework**: asyncio
- **HTTP Client**: httpx (async)
- **Telegram Integration**: python-telegram-bot
- **Retry Logic**: tenacity
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest, pytest-asyncio, coverage

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.11 or higher
- **RAM**: 256 MB minimum, 512 MB recommended
- **Storage**: 100 MB for application + dependencies
- **Network**: Stable internet connection for API calls
- **Operating System**: Linux, macOS, or Windows (with WSL for Windows)

### Recommended Requirements
- **Python**: 3.12+
- **RAM**: 1 GB
- **Storage**: 1 GB
- **Network**: Low latency connection to OpenHands API and Telegram
- **CPU**: 2+ cores for optimal performance

### Dependencies

#### Core Dependencies
- `python-telegram-bot>=20.0` - Telegram Bot API integration
- `httpx>=0.25.0` - Async HTTP client for API calls
- `tenacity>=8.2.0` - Retry decorator for robust API calls
- `asyncio` - Built-in async framework (Python 3.11+)

#### Development Dependencies
- `pytest>=7.4.0` - Testing framework
- `pytest-asyncio>=0.21.0` - Async test support
- `pytest-cov>=4.1.0` - Test coverage reporting
- `coverage>=7.3.0` - Code coverage analysis

## 📥 Installation Guide

### Prerequisites
1. **Python 3.11+** installed and available in PATH
2. **Git** for version control and cloning repository
3. **Docker and Docker Compose** (optional, for containerized deployment)
4. **Telegram Bot Token** from [@BotFather](https://t.me/botfather)
5. **Telegram Chat ID** for notifications (user, group, or channel)

### Installation Methods

#### Method 1: Manual Installation (Recommended for Development)

```bash
# 1. Clone the repository
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

#### Method 2: Docker Installation (Recommended for Production)

```bash
# 1. Clone the repository
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# 2. Build Docker image
docker build -t openhands-monitor .

# 3. Or use Docker Compose
docker-compose build
```

#### Method 3: Development Installation (with Testing Tools)

```bash
# 1. Clone and setup for development
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install all dependencies including development tools
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov coverage
```

### Environment Setup

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file** with your configuration:
   ```bash
   nano .env  # or use your preferred text editor
   ```

3. **Configure the required variables** (see Configuration section below)

## ⚙️ Configuration

### Environment Variables

The bot is configured through environment variables, which can be set in a `.env` file or directly in the environment.

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `TELEGRAM_TOKEN` | Telegram Bot API token | **Yes** | None | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `CHAT_ID` | Telegram chat/channel ID | **Yes** | None | `-1001234567890` |
| `OPENHANDS_API_URL` | OpenHands API endpoint | No | `http://host.docker.internal:3000` | `http://localhost:3000` |
| `POLL_INTERVAL` | Polling interval in seconds | No | `5` | `10` |

### Obtaining Telegram Credentials

#### 1. Get Telegram Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create a new bot
4. Copy the token provided (format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### 2. Get Chat ID
1. For personal notifications: Use [@userinfobot](https://t.me/userinfobot)
2. For group/channel notifications:
   - Add your bot to the group/channel
   - Send a message in the group/channel
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find the `chat.id` in the response

### Example `.env` File

```env
# OpenHands Monitor Bot Configuration
# ===================================

# Required: Telegram Bot Configuration
# Get from @BotFather on Telegram
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Required: Telegram chat ID (user, group, or channel)
# Use @userinfobot on Telegram to find your chat ID
CHAT_ID=-1001234567890

# Optional: OpenHands API Configuration
# Default: http://host.docker.internal:3000
OPENHANDS_API_URL=http://localhost:3000

# Optional: Polling interval in seconds
# Default: 5 seconds
POLL_INTERVAL=5
```

### Application Configuration

#### Polling Configuration
The polling interval can be configured via the `POLL_INTERVAL` environment variable:
- **Default**: 5 seconds
- **Minimum**: 1 second (be mindful of API rate limits)
- **Recommended**: 5-30 seconds depending on monitoring needs

#### Telegram Configuration
- **Bot Permissions**: Ensure the bot has permission to send messages
- **Chat Settings**: Bot must be added to the target chat/channel
- **Rate Limits**: Respect Telegram API rate limits (30 messages/second)

#### API Configuration
- **Timeout Settings**: HTTP requests timeout after 30 seconds
- **Retry Logic**: 3 retry attempts with 2-second delays
- **Error Handling**: Graceful degradation on API failures

### Security Configuration
- **Secret Management**: Always use environment variables or secret managers
- **Network Security**: Use HTTPS for API endpoints in production
- **Access Control**: Restrict API access where possible
- **Logging**: Configure appropriate log levels for production (INFO or WARNING)

## 🚀 Usage

### Starting the Bot

#### Method 1: Direct Python Execution
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Start the bot
python bot.py
```

#### Method 2: Docker Execution
```bash
# Run with Docker
docker run -d \
  --name openhands-monitor \
  --network host \
  --env-file .env \
  openhands-monitor

# Or with Docker Compose
docker-compose up -d
```

### Bot Startup Sequence

When started, the bot performs the following sequence:

1. **Configuration Validation**: Checks that all required environment variables are set
2. **Startup Notification**: Sends "🤖 OpenHands Monitor Bot is online and starting to poll." to Telegram
3. **Initial Poll**: Fetches current conversations from OpenHands API
4. **State Initialization**: Stores initial conversation states
5. **Continuous Monitoring**: Begins polling at configured interval

### Monitoring Output

The bot provides real-time logging:

```
2024-01-13 20:30:45 - bot - INFO - Starting polling loop...
2024-01-13 20:30:50 - bot - INFO - Fetched 5 conversations from OpenHands API
2024-01-13 20:30:50 - bot - INFO - Sent Telegram notification: New Task Started
```

### Notification Examples

#### New Task Notification
```
🆕 New Task Started: Data Analysis Pipeline (ID: conv_abc123)
```

#### Status Update Notification
```
🔄 Task Status Update: Model Training is now completed.
```

#### Multiple Changes
If multiple changes occur between polling cycles, the bot sends separate notifications for each change.

### Stopping the Bot

#### Graceful Shutdown
```bash
# For Python execution
Ctrl+C

# For Docker
docker stop openhands-monitor

# For Docker Compose
docker-compose down
```

## 📚 API Documentation

### OpenHands Monitor Bot API

#### Core Functions

##### `get_definitions(word: str, custom_dict: dict = None) -> list`
**Location**: `map_maker.py`

**Description**: Retrieves definitions for a word from a dictionary.

**Parameters**:
- `word` (str): Word to look up. Automatically converted to string if not already.
- `custom_dict` (dict, optional): Custom dictionary to use instead of standard dictionary.

**Returns**:
- `list`: List of definitions. Empty list if word not found.

**Examples**:
```python
from map_maker import get_definitions

# Standard dictionary lookup
definitions = get_definitions("apple")
# Returns: ['A fruit that grows on trees', 'A technology company founded by Steve Jobs']

# Custom dictionary lookup
custom_dict = {"python": ["My favorite programming language"]}
definitions = get_definitions("python", custom_dict)
# Returns: ['My favorite programming language']

# Word not found
definitions = get_definitions("nonexistent")
# Returns: []
```

**Error Handling**:
- Non-string inputs are converted to strings
- Empty strings return empty lists
- None values are converted to "none" string
- Returns copy of list to prevent mutation of original dictionary

##### `send_telegram_message(message: str) -> bool`
**Location**: `bot.py`

**Description**: Sends a message to configured Telegram chat.

**Parameters**:
- `message` (str): Message text to send.

**Returns**:
- `bool`: True if message sent successfully, False otherwise.

**Error Handling**:
- Retries 3 times with 2-second delays
- Logs errors on failure
- Raises exception after retries exhausted

##### `fetch_conversations() -> list[dict]`
**Location**: `bot.py`

**Description**: Fetches conversations from OpenHands API.

**Parameters**: None

**Returns**:
- `list[dict]` or `[]`: List of conversations or empty list on error.

**Error Handling**:
- Handles HTTP errors gracefully
- Returns empty list on network failures
- Logs error details

##### `poll_and_notify() -> None`
**Location**: `bot.py`

**Description**: Main polling loop for monitoring conversations.

**Parameters**: None

**Returns**: None (runs indefinitely)

**Behavior**:
- Polls API at configured interval
- Compares current state with previous state
- Sends notifications for changes
- Cleans up old conversation states

##### `main() -> None`
**Location**: `bot.py`

**Description**: Main entry point for the OpenHands Monitor Bot.

**Parameters**: None

**Returns**: None

**Behavior**:
- Validates environment variables
- Sends startup notification
- Starts polling loop
- Handles graceful shutdown

### Standard Dictionary API

The standard dictionary (`STANDARD_DICTIONARY`) contains:

| Word | Definitions |
|------|-------------|
| `apple` | 1. "A fruit that grows on trees"<br>2. "A technology company founded by Steve Jobs" |
| `python` | 1. "A high-level programming language"<br>2. "A large constricting snake" |
| `openhands` | "A platform for AI development and collaboration" |
| `test` | 1. "A procedure intended to establish the quality, performance, or reliability of something"<br>2. "An examination of someone's knowledge or proficiency" |
| `hello` | 1. "A greeting or expression of goodwill"<br>2. "Used to attract attention" |
| `world` | 1. "The earth, together with all of its countries and peoples"<br>2. "A particular region or group of countries" |

### Telegram Notification Format

#### New Task Notification
```
🆕 New Task Started: {title} (ID: {conv_id})
```

#### Status Update Notification
```
🔄 Task Status Update: {title} is now {status}.
```

#### Startup Notification
```
🤖 OpenHands Monitor Bot is online and starting to poll.
```

## 🐳 Docker Deployment

### Docker Configuration

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

CMD ["python", "bot.py"]
```

#### Docker Compose Configuration
```yaml
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

### Building Docker Images

#### Basic Build
```bash
# Build image
docker build -t openhands-monitor .

# Tag for registry
docker tag openhands-monitor:latest your-registry/openhands-monitor:1.0.0
```

#### Multi-stage Build (Optional Enhancement)
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY bot.py .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "bot.py"]
```

### Running Containers

#### Basic Run
```bash
# Run container
docker run -d \
  --name openhands-monitor \
  --network host \
  -e TELEGRAM_TOKEN="your_token" \
  -e CHAT_ID="your_chat_id" \
  openhands-monitor
```

#### Docker Compose Run
```bash
# Create .env file
echo "TELEGRAM_TOKEN=your_token" > .env
echo "CHAT_ID=your_chat_id" >> .env

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Container Management

#### Monitoring Containers
```bash
# Check container status
docker ps -a | grep openhands-monitor

# View logs
docker logs openhands-monitor

# View resource usage
docker stats openhands-monitor

# Execute commands in container
docker exec -it openhands-monitor /bin/bash
```

#### Container Maintenance
```bash
# Stop container
docker stop openhands-monitor

# Remove container
docker rm openhands-monitor

# Remove image
docker rmi openhands-monitor

# Clean up unused resources
docker system prune -a
```

### Production Deployment

#### Security Hardening
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  openhands-monitor:
    build: .
    container_name: openhands-monitor-prod
    user: "1000:1000"  # Non-root user
    restart: unless-stopped
    network_mode: bridge
    ports:
      - "127.0.0.1:3000:3000"  # Bind to localhost only
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - CHAT_ID=${CHAT_ID}
      - OPENHANDS_API_URL=http://localhost:3000
    volumes:
      - ./logs:/app/logs  # Persistent logs
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

#### Health Checks
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## 🧪 Testing

### Test Architecture

#### Test Structure
```
tests/
├── __init__.py
├── test_bot.py          # Tests for main bot functionality
└── test_map_maker.py    # Comprehensive tests for dictionary module
```

### Test Categories

#### 1. Unit Tests for `map_maker.py`
- **Basic Functionality**: Standard dictionary lookups
- **Edge Cases**: Empty strings, None values, whitespace
- **Custom Dictionaries**: User-provided dictionary functionality
- **Type Safety**: Handling of non-string inputs
- **Performance**: Large dictionary performance
- **Unicode Support**: International character handling

#### 2. Integration Tests for `bot.py`
- **API Integration**: OpenHands API interaction
- **Telegram Integration**: Message sending functionality
- **State Management**: Conversation state tracking
- **Error Handling**: Network failures and API errors

### Running Tests

#### Basic Test Execution
```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_map_maker.py

# Run specific test class
python -m pytest tests/test_map_maker.py::TestGetDefinitions
```

#### Test Coverage
```bash
# Generate coverage report
python -m pytest tests/ --cov=map_maker --cov-report=html

# View coverage in terminal
python -m pytest tests/ --cov=map_maker --cov-report=term-missing

# Minimum coverage requirement
python -m pytest tests/ --cov=map_maker --cov-fail-under=95
```

#### Test Configuration
- **Test Discovery**: Automatically discovers tests in `tests/` directory
- **Test Isolation**: Each test runs in isolated environment
- **Async Support**: `pytest-asyncio` for async function testing
- **Fixture Support**: Reusable test fixtures for common setup

### Test Examples

#### Example Unit Test
```python
def test_basic_functionality():
    """Test basic dictionary lookup functionality."""
    result = get_definitions("apple")
    expected = [
        "A fruit that grows on trees",
        "A technology company founded by Steve Jobs"
    ]
    assert result == expected
```

#### Example Integration Test
```python
@pytest.mark.asyncio
async def test_send_telegram_message():
    """Test Telegram message sending functionality."""
    # Mock Telegram API
    with patch('bot.bot.send_message') as mock_send:
        await send_telegram_message("Test message")
        mock_send.assert_called_once()
```

### Continuous Integration

#### GitHub Actions Configuration
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov coverage
      - name: Run tests
        run: python -m pytest tests/ --cov=map_maker --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 🛠️ Development

### Project Structure
```
openhands-monitor-bot/
├── bot.py                    # Main monitoring bot
├── map_maker.py              # Dictionary module
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── README.md                # This documentation file
├── TECHNICAL_DOCUMENTATION.md # Detailed technical docs
├── LICENSE                  # MIT License
└── tests/                   # Test suite
    ├── __init__.py
    ├── test_bot.py
    └── test_map_maker.py
```

### Development Setup
```bash
# 1. Clone repository
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov coverage black isort

# 4. Set up pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Code Style
- **Formatting**: Use Black for code formatting
- **Imports**: Use isort for import sorting
- **Linting**: Follow PEP 8 guidelines
- **Type Hints**: Use Python type hints for better code clarity
- **Docstrings**: Follow Google-style docstrings

### Running Code Quality Tools
```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Run linter
flake8 .

# Run type checking (if using mypy)
mypy .
```

### Adding New Features
1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Implement the feature with tests
3. Run tests: `python -m pytest tests/`
4. Ensure code coverage remains above 95%
5. Update documentation if needed
6. Create a pull request

## 🔧 Troubleshooting

### Common Issues

#### Issue 1: Telegram Token Not Working
**Symptoms**: Bot fails to start with "Configuration error"
**Solution**:
1. Verify token format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
2. Ensure bot is started with @BotFather
3. Check that bot has permission to send messages

#### Issue 2: Chat ID Not Found
**Symptoms**: Messages not delivered to Telegram
**Solution**:
1. Use @userinfobot to get personal chat ID
2. For groups/channels: Add bot first, then get chat ID from API
3. Verify bot is added to the target chat

#### Issue 3: OpenHands API Connection Failed
**Symptoms**: "HTTP error fetching conversations" in logs
**Solution**:
1. Check OPENHANDS_API_URL is correct
2. Verify OpenHands API is running
3. Check network connectivity
4. Verify API endpoint `/api/conversations` exists

#### Issue 4: High CPU/Memory Usage
**Symptoms**: System slowing down
**Solution**:
1. Increase POLL_INTERVAL (e.g., from 5 to 30 seconds)
2. Monitor with `docker stats` or system monitoring tools
3. Check for memory leaks in conversation_states

#### Issue 5: Duplicate Notifications
**Symptoms**: Same notification sent multiple times
**Solution**:
1. Check if OpenHands API is returning duplicate conversations
2. Verify conversation_states cleanup is working
3. Check polling interval isn't too short

### Logging Levels
- **DEBUG**: Detailed debugging information
- **INFO**: General operational information (default)
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failed operations
- **CRITICAL**: Critical errors requiring immediate attention

### Debug Mode
Enable debug logging for troubleshooting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

We welcome contributions to the OpenHands Monitor Bot! Here's how you can help:

### How to Contribute
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Contribution Guidelines
- **Code Quality**: Ensure code follows project standards
- **Testing**: Include tests for new features
- **Documentation**: Update README.md and docstrings
- **Backward Compatibility**: Don't break existing functionality
- **Security**: Follow security best practices

### Areas for Contribution
- **New Features**: Additional monitoring capabilities
- **Bug Fixes**: Fix reported issues
- **Documentation**: Improve documentation
- **Tests**: Add more test coverage
- **Performance**: Optimize existing code
- **Security**: Security enhancements

### Reporting Issues
When reporting issues, please include:
1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Step-by-step reproduction instructions
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: OS, Python version, dependencies
6. **Logs**: Relevant log output

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- **Permissions**: Commercial use, modification, distribution, private use
- **Conditions**: License and copyright notice must be included
- **Limitations**: No liability, no warranty

### Third-Party Licenses
- **python-telegram-bot**: LGPLv3
- **httpx**: BSD 3-Clause
- **tenacity**: Apache 2.0
- **pytest**: MIT

## 📞 Support

### Getting Help
- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: Check this README and TECHNICAL_DOCUMENTATION.md
- **Community**: OpenHands community forums

### Resources
- [OpenHands Platform Documentation](https://docs.openhands.dev)
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

### Acknowledgments
- Thanks to the OpenHands team for creating the platform
- Thanks to the python-telegram-bot maintainers
- Thanks to all contributors who have helped improve this project

---

**OpenHands Monitor Bot** - Keeping your team informed, one notification at a time! 🚀



