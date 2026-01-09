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

## Monitoring and Logging

### Logging Configuration

#### Log Levels
- **INFO**: Normal operational messages
- **WARNING**: Non-critical issues that may require attention
- **ERROR**: Critical errors that affect functionality
- **DEBUG**: Detailed debugging information (enable for troubleshooting)

#### Log Output
```python
# Example log output format
2026-01-09 12:30:45 INFO - Starting polling loop...
2026-01-09 12:30:50 INFO - Fetched 5 conversations from API
2026-01-09 12:30:50 INFO - New task detected: "Разработка нового функционала"
2026-01-09 12:30:51 INFO - Telegram notification sent successfully
2026-01-09 12:30:55 WARNING - API request timeout, retrying...
2026-01-09 12:30:57 ERROR - Failed to send Telegram message after 3 attempts
```

### Monitoring Metrics

#### Key Performance Indicators (KPIs)
1. **API Response Time**: Time to fetch conversations from OpenHands API
2. **Notification Success Rate**: Percentage of successful Telegram message deliveries
3. **Polling Interval Consistency**: Consistency of polling intervals
4. **Memory Usage**: RAM consumption over time
5. **Error Rate**: Frequency of different error types

#### Health Checks
```bash
# Basic health check
curl http://localhost:3000/health  # If health endpoint exists

# Container health check
docker inspect openhands-monitor --format='{{.State.Health.Status}}'

# Process health check
ps aux | grep "python bot.py" | grep -v grep
```

### Log Management

#### Log Rotation
```bash
# Manual log rotation
docker logs openhands-monitor > bot_$(date +%Y%m%d).log
docker-compose logs --no-color > logs_$(date +%Y%m%d_%H%M%S).txt

# Automated log rotation with logrotate
# /etc/logrotate.d/openhands-monitor
/var/log/openhands-monitor/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}
```

#### Centralized Logging
- **ELK Stack**: Elasticsearch, Logstash, Kibana
- **Splunk**: Enterprise log management
- **Graylog**: Open-source log management
- **Cloud Services**: AWS CloudWatch, Google Cloud Logging, Azure Monitor

## Security Considerations

### Security Best Practices

#### 1. Secret Management
- **Never commit secrets** to version control
- Use environment variables or secret managers (Hashicorp Vault, AWS Secrets Manager)
- Rotate Telegram tokens regularly
- Use different tokens for development and production

#### 2. Network Security
- Use HTTPS for all API endpoints
- Implement firewall rules to restrict access
- Use VPN for internal API access
- Monitor network traffic for anomalies

#### 3. Container Security
- Run containers as non-root users
- Use minimal base images
- Regularly update base images and dependencies
- Scan images for vulnerabilities
- Implement resource limits

#### 4. API Security
- Validate all API responses
- Implement rate limiting
- Use API keys or tokens for authentication
- Monitor API usage patterns

### Security Configuration Examples

#### Secure Docker Compose Configuration
```yaml
version: '3.8'
services:
  openhands-monitor:
    build: .
    container_name: openhands-monitor-secure
    user: "1000:1000"  # Non-root user
    restart: unless-stopped
    network_mode: bridge
    ports:
      - "127.0.0.1:3000:3000"  # Localhost binding only
    environment:
      - TELEGRAM_TOKEN_FILE=/run/secrets/telegram_token
      - CHAT_ID_FILE=/run/secrets/chat_id
    secrets:
      - telegram_token
      - chat_id
    security_opt:
      - no-new-privileges:true
      - seccomp=unconfined
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE

secrets:
  telegram_token:
    file: ./secrets/telegram_token.txt
  chat_id:
    file: ./secrets/chat_id.txt
```

#### Security Scanning
```bash
# Scan Docker image for vulnerabilities
docker scan openhands-monitor

# Check for outdated dependencies
pip list --outdated

# Security audit with bandit
pip install bandit
bandit -r . -f json -o bandit-report.json
```

## Performance Optimization

### Optimization Strategies

#### 1. Polling Optimization
- **Adjust Polling Interval**: Increase from 5 seconds to 30-60 seconds for production
- **Implement Exponential Backoff**: For API failures
- **Batch Processing**: Process multiple conversations in batches
- **Caching**: Cache API responses when appropriate

#### 2. Memory Optimization
- **State Management**: Implement periodic state cleanup
- **Connection Pooling**: Reuse HTTP connections
- **Garbage Collection**: Configure Python garbage collection
- **Memory Limits**: Set container memory limits

#### 3. Network Optimization
- **Connection Keep-Alive**: Reuse TCP connections
- **Compression**: Enable HTTP compression
- **DNS Caching**: Cache DNS lookups
- **Timeout Configuration**: Optimize timeout values

### Performance Monitoring

#### Resource Monitoring
```bash
# Monitor container resources
docker stats openhands-monitor

# Monitor process resources
top -p $(pgrep -f "python bot.py")

# Monitor network connections
netstat -tulpn | grep python
```

#### Performance Testing
```bash
# Load testing with Apache Bench
ab -n 1000 -c 10 http://localhost:3000/api/conversations

# Memory profiling with memory_profiler
python -m memory_profiler bot.py

# CPU profiling with cProfile
python -m cProfile -o profile.stats bot.py
```

### Scaling Strategies

#### Horizontal Scaling
```yaml
# Docker Swarm scaling
docker service scale openhands-monitor=3

# Kubernetes scaling
kubectl scale deployment openhands-monitor --replicas=3
```

#### Load Balancing
- **Round Robin**: Distribute requests evenly
- **Least Connections**: Send to server with fewest connections
- **Session Affinity**: Maintain user sessions on same server

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Bot Won't Start
**Symptoms**: Bot fails to start or exits immediately
**Possible Causes**:
1. Missing environment variables
2. Invalid Telegram token
3. Network connectivity issues

**Solutions**:
```bash
# Check environment variables
echo "TELEGRAM_TOKEN: $TELEGRAM_TOKEN"
echo "CHAT_ID: $CHAT_ID"

# Test Telegram API
curl "https://api.telegram.org/bot${TELEGRAM_TOKEN}/getMe"

# Test OpenHands API connectivity
curl "${OPENHANDS_API_URL}/api/conversations"
```

#### Issue 2: No Telegram Notifications
**Symptoms**: Bot runs but no messages received
**Possible Causes**:
1. Incorrect Chat ID
2. Bot not added to chat
3. Telegram API issues

**Solutions**:
```bash
# Verify Chat ID
curl "https://api.telegram.org/bot${TELEGRAM_TOKEN}/getUpdates"

# Check bot permissions
# Ensure bot has permission to send messages in the chat
```

#### Issue 3: High Resource Usage
**Symptoms**: High CPU or memory consumption
**Possible Causes**:
1. Too frequent polling (5-second interval)
2. Memory leaks
3. Large conversation sets

**Solutions**:
```bash
# Increase polling interval (edit bot.py)
# Change POLL_INTERVAL from 5 to 30 seconds

# Monitor resource usage
docker stats openhands-monitor

# Restart container periodically
docker restart openhands-monitor
```

#### Issue 4: API Connection Errors
**Symptoms**: Frequent timeouts or connection errors
**Possible Causes**:
1. Network issues
2. API downtime
3. Firewall restrictions

**Solutions**:
```bash
# Test network connectivity
ping $(echo $OPENHANDS_API_URL | sed 's|http://||' | sed 's|https://||' | cut -d/ -f1)

# Check API status
curl -I $OPENHANDS_API_URL

# Implement retry logic (already built-in)
```

### Debug Mode

#### Enable Debug Logging
```bash
# Run with debug output
export PYTHONUNBUFFERED=1
python -u bot.py 2>&1 | tee debug.log

# Or with increased verbosity
python -c "import logging; logging.basicConfig(level=logging.DEBUG)" bot.py
```

#### Interactive Debugging
```python
# Add debug statements to bot.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use pdb for interactive debugging
import pdb
pdb.set_trace()  # Add this line where you want to debug
```

## Development Guidelines

### Code Standards

#### Python Style Guide
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) conventions
- Use meaningful variable and function names
- Add docstrings for all public functions and classes
- Keep functions small and focused (single responsibility)

#### Example Code Structure
```python
def process_conversation(conversation: dict) -> str:
    """
    Process a single conversation and return notification message.
    
    Args:
        conversation (dict): Conversation data from API
        
    Returns:
        str: Formatted notification message
        
    Raises:
        ValueError: If conversation data is invalid
    """
    if not conversation.get("id"):
        raise ValueError("Conversation must have an ID")
    
    title = conversation.get("title", "Untitled")
    conv_id = conversation["id"]
    
    return f"🆕 New Task Started: {title} (ID: {conv_id})"
```

### Project Structure

#### Recommended Structure
```
openhands-monitor-bot/
├── src/                    # Source code
│   ├── __init__.py
│   ├── bot.py             # Main bot module
│   ├── map_maker.py       # Dictionary module
│   └── utils/             # Utility functions
│       ├── __init__.py
│       ├── logging.py     # Logging configuration
│       └── config.py      # Configuration management
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_bot.py
│   └── test_map_maker.py
├── docs/                   # Documentation
│   ├── api.md
│   └── deployment.md
├── scripts/                # Utility scripts
│   ├── setup.sh
│   └── deploy.sh
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
└── TECHNICAL_DOCUMENTATION.md  # This file
```

### Development Workflow

#### 1. Setup Development Environment
```bash
# Clone repository
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .  # Install in development mode
```

#### 2. Make Changes
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make code changes
# Add tests for new functionality
# Update documentation
```

#### 3. Test Changes
```bash
# Run tests
python -m pytest tests/ -v

# Check code style
pip install black flake8
black src/ tests/
flake8 src/ tests/

# Run type checking (optional)
pip install mypy
mypy src/
```

#### 4. Submit Changes
```bash
# Commit changes
git add .
git commit -m "Add new feature: description"

# Push to remote
git push origin feature/new-feature

# Create pull request
# Wait for code review and CI checks
```

### Dependency Management

#### Updating Dependencies
```bash
# Update all dependencies
pip install --upgrade -r requirements.txt

# Generate new requirements.txt
pip freeze > requirements.txt

# Check for security vulnerabilities
pip install safety
safety check -r requirements.txt
```

#### Version Pinning
```txt
# requirements.txt with version pinning
python-telegram-bot==20.7
httpx==0.25.2
tenacity==8.2.3
pytest==7.4.4
pytest-asyncio==0.21.1
```

## Contributing

### Contribution Guidelines

#### How to Contribute
1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run the test suite**: `python -m pytest tests/`
5. **Ensure code quality**: Follow PEP 8 and add docstrings
6. **Submit a pull request** with clear description

#### Code Review Process
1. **Automated Checks**: CI/CD pipeline runs tests and checks
2. **Manual Review**: Maintainers review code for quality and functionality
3. **Feedback**: Address any feedback or requested changes
4. **Merge**: Once approved, changes are merged to main branch

### Issue Reporting

#### Bug Reports
When reporting bugs, include:
- **Description**: Clear description of the issue
- **Steps to Reproduce**: Exact steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: Python version, OS, dependencies
- **Logs**: Relevant error logs or screenshots

#### Feature Requests
When requesting features, include:
- **Use Case**: How the feature would be used
- **Benefits**: Why the feature is valuable
- **Implementation Ideas**: Suggestions for implementation (optional)
- **Alternatives**: Any alternative solutions considered

### Community Guidelines

#### Code of Conduct
- **Be respectful**: Treat all contributors with respect
- **Be inclusive**: Welcome contributors from all backgrounds
- **Be constructive**: Provide constructive feedback
- **Be patient**: Allow time for review and discussion

#### Communication Channels
- **GitHub Issues**: For bug reports and feature requests
- **Pull Requests**: For code contributions
- **Documentation**: For improving documentation
- **Discussions**: For questions and discussions (if enabled)

### Recognition

#### Contributors
All contributors are recognized in:
- **GitHub Contributors list**
- **Project README** (for significant contributions)
- **Release notes** (for each release)

#### Attribution
When using code from this project:
- **Credit the original authors**
- **Include the MIT license**
- **Link to the original repository**

---

## Conclusion

This technical documentation provides comprehensive guidance for installing, configuring, using, and maintaining the OpenHands Monitor Bot. The documentation covers:

1. **Project Overview**: Understanding the system architecture and components
2. **Installation**: Multiple installation methods for different environments
3. **Configuration**: Environment variables and application settings
4. **API Documentation**: Detailed API reference for all functions
5. **Testing**: Comprehensive testing strategy and procedures
6. **Docker Deployment**: Containerized deployment with security best practices
7. **Monitoring**: Logging, monitoring, and performance optimization
8. **Security**: Security considerations and hardening guidelines
9. **Troubleshooting**: Common issues and solutions
10. **Development**: Guidelines for contributing and extending the project

### Maintenance and Updates

#### Regular Maintenance Tasks
- **Weekly**: Check for dependency updates
- **Monthly**: Review logs and performance metrics
- **Quarterly**: Security audit and vulnerability scanning
- **Annually**: Major version review and architecture assessment

#### Update Procedures
1. **Backup**: Always backup configuration and data before updates
2. **Test**: Test updates in staging environment first
3. **Document**: Update documentation with changes
4. **Communicate**: Notify users of breaking changes
5. **Monitor**: Closely monitor after deployment

### Support

#### Getting Help
- **Documentation**: First check this documentation and README
- **GitHub Issues**: Report bugs or ask questions
- **Community**: Engage with other users (if community exists)

#### Professional Support
For enterprise or professional support needs:
- **Custom Development**: Feature development and customization
- **Integration**: Integration with other systems
- **Consulting**: Architecture and deployment consulting
- **Training**: Team training and knowledge transfer

---

*Documentation Version: 1.0.0*  
*Last Updated: 2026-01-09*  
*Maintained by: OpenHands Development Team*