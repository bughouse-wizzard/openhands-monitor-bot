# OpenHands Monitor Bot - Technical Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [System Requirements](#system-requirements)
4. [Installation Guide](#installation-guide)
5. [Configuration](#configuration)
6. [API Documentation](#api-documentation)
7. [Testing Strategy](#testing-strategy)
8. [Docker Deployment](#docker-deployment)
9. [Monitoring and Logging](#monitoring-and-logging)
10. [Security Considerations](#security-considerations)
11. [Performance Optimization](#performance-optimization)
12. [Troubleshooting](#troubleshooting)
13. [Development Guidelines](#development-guidelines)
14. [Contributing](#contributing)

## Project Overview

OpenHands Monitor Bot is a monitoring system designed to track task changes in the OpenHands platform and send notifications to Telegram. The system consists of two main components:

1. **Main Monitoring Module (`bot.py`)**: An asynchronous bot that polls the OpenHands API for conversation/task changes and sends notifications to Telegram.
2. **Dictionary Module (`map_maker.py`)**: A utility module for word definitions with a standard dictionary and support for custom dictionaries.

### Key Features
- Real-time monitoring of OpenHands task status changes
- Telegram notifications for new tasks and status updates
- Configurable polling intervals
- Docker containerization for easy deployment
- Comprehensive test coverage
- Modular architecture for extensibility

## Architecture

### System Architecture Diagram
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
- **Error Handling**: Retry mechanisms and error recovery

#### 2. Dictionary Module (`map_maker.py`)
- **Dictionary Interface**: Standard dictionary with common word definitions
- **Search Function**: Case-insensitive word lookup with normalization
- **Custom Dictionary Support**: Extensible with user-provided dictionaries
- **Type Safety**: Robust handling of various input types

### Data Flow
1. **Polling**: Bot queries OpenHands API for current conversations
2. **Comparison**: Compares current state with previous state stored in memory
3. **Detection**: Identifies new conversations and status changes
4. **Notification**: Sends appropriate messages to Telegram
5. **State Update**: Updates internal state tracking

### Technology Stack
- **Language**: Python 3.11+
- **Async Framework**: asyncio
- **HTTP Client**: httpx (async)
- **Telegram Integration**: python-telegram-bot
- **Retry Logic**: tenacity
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest, pytest-asyncio, coverage

## System Requirements

### Minimum Requirements
- **Python**: 3.11 or higher
- **RAM**: 256 MB minimum, 512 MB recommended
- **Storage**: 100 MB for application + dependencies
- **Network**: Stable internet connection for API calls

### Recommended Requirements
- **Python**: 3.12+
- **RAM**: 1 GB
- **Storage**: 1 GB
- **Network**: Low latency connection to OpenHands API and Telegram

### Dependencies
#### Core Dependencies
- `python-telegram-bot>=20.0` - Telegram Bot API integration
- `httpx>=0.25.0` - Async HTTP client
- `tenacity>=8.2.0` - Retry decorator for robust API calls
- `asyncio` - Built-in async framework

#### Development Dependencies
- `pytest>=7.4.0` - Testing framework
- `pytest-asyncio>=0.21.0` - Async test support
- `pytest-cov>=4.1.0` - Test coverage reporting
- `coverage>=7.3.0` - Code coverage analysis

## Installation Guide

### Prerequisites
1. Python 3.11+ installed
2. Git for version control
3. Docker and Docker Compose (for containerized deployment)
4. Telegram Bot Token from @BotFather
5. Telegram Chat ID for notifications

### Installation Methods

#### Method 1: Manual Installation
```bash
# Clone the repository
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Method 2: Docker Installation
```bash
# Clone the repository
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# Build Docker image
docker build -t openhands-monitor .

# Or use Docker Compose
docker-compose build
```

#### Method 3: Development Installation
```bash
# Clone and setup for development
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install all dependencies including development tools
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov coverage
```

### Environment Setup
Create a `.env` file in the project root:
```bash
TELEGRAM_TOKEN=your_telegram_bot_token_here
CHAT_ID=your_telegram_chat_id_here
OPENHANDS_API_URL=http://localhost:3000  # or your OpenHands API URL
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `TELEGRAM_TOKEN` | Telegram Bot API token | Yes | None | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `CHAT_ID` | Telegram chat/channel ID | Yes | None | `-1001234567890` |
| `OPENHANDS_API_URL` | OpenHands API endpoint | No | `http://host.docker.internal:3000` | `http://localhost:3000` |

### Application Configuration

#### Polling Configuration
The polling interval is hardcoded in `bot.py`:
```python
POLL_INTERVAL = 5  # seconds
```
To change the interval, modify this value in the source code.

#### Telegram Configuration
- **Bot Permissions**: Ensure the bot has permission to send messages
- **Chat Settings**: Bot must be added to the target chat/channel
- **Rate Limits**: Respect Telegram API rate limits (30 messages/second)

#### API Configuration
- **Timeout Settings**: HTTP requests timeout after 30 seconds
- **Retry Logic**: 3 retry attempts with 2-second delays
- **Error Handling**: Graceful degradation on API failures

### Security Configuration
- **Secret Management**: Use environment variables or secret managers
- **Network Security**: Use HTTPS for API endpoints
- **Access Control**: Restrict API access where possible
- **Logging**: Configure appropriate log levels for production

## API Documentation

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

##### `send_telegram_message(message: str)`
**Location**: `bot.py`

**Description**: Sends a message to configured Telegram chat.

**Parameters**:
- `message` (str): Message text to send.

**Returns**: None

**Error Handling**:
- Retries 3 times with 2-second delays
- Logs errors on failure
- Raises exception after retries exhausted

##### `fetch_conversations() -> list`
**Location**: `bot.py`

**Description**: Fetches conversations from OpenHands API.

**Parameters**: None

**Returns**:
- `list` or `None`: List of conversations or None on error.

**Error Handling**:
- Handles HTTP errors gracefully
- Returns None on network failures
- Logs error details

##### `poll_and_notify()`
**Location**: `bot.py`

**Description**: Main polling loop for monitoring conversations.

**Parameters**: None

**Returns**: None (runs indefinitely)

**Behavior**:
- Polls API at configured interval
- Compares current state with previous state
- Sends notifications for changes
- Cleans up old conversation states

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

## Testing Strategy

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

## Docker Deployment

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
      - OPENHANDS_API_URL=https://api.openhands.example.com
    security_opt:
      - no-new-privileges:true
    read_only: true  # Read-only filesystem
    tmpfs:
      - /tmp  # Temporary directory
```

#### High Availability Configuration
```yaml
# docker-compose.ha.yml
version: '3.8'
services:
  openhands-monitor:
    image: openhands-monitor:latest
    deploy:
      mode: replicated
      replicas: 2
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - CHAT_ID=${CHAT_ID}
      - OPENHANDS_API_URL=${OPENHANDS_API_URL}
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Kubernetes Deployment

#### Deployment Configuration
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: openhands-monitor
spec:
  replicas: 2
  selector:
    matchLabels:
      app: openhands-monitor
  template:
    metadata:
      labels:
        app: openhands-monitor
    spec:
      containers:
      - name: openhands-monitor
        image: openhands-monitor:latest
        env:
        - name: TELEGRAM_TOKEN
          valueFrom:
            secretKeyRef:
              name: telegram-secrets
              key: token
        - name: CHAT_ID
          valueFrom:
            secretKeyRef:
              name: telegram-secrets
              key: chat-id
        - name: OPENHANDS_API_URL
          value: "https://api.openhands.example.com"
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          exec:
            command: ["python", "-c", "import sys; sys.exit(0)"]
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command: ["python", "-c", "import sys; sys.exit(0)"]
          initialDelaySeconds: 5
          periodSeconds: 5
```