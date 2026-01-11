# OpenHands Monitor Bot

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

A Telegram bot for monitoring OpenHands platform tasks and sending real-time notifications about task status changes.

## 🚀 Getting Started

The OpenHands Monitor Bot is a Python application that continuously monitors OpenHands platform tasks and sends real-time notifications to Telegram when task statuses change. It's designed to help developers and administrators stay informed about their OpenHands tasks without constantly checking the platform.

## 📋 Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)

## Installation

### Prerequisites
- Python 3.11 or higher
- Docker and Docker Compose (optional, for containerization)
- Telegram account with a bot created via [@BotFather](https://t.me/botfather)

### Step-by-Step Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
   cd openhands-monitor-bot
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the project root with the following variables:
   ```bash
   TELEGRAM_TOKEN=your_telegram_bot_token
   CHAT_ID=your_telegram_chat_id
   OPENHANDS_API_URL=http://localhost:3000  # or your OpenHands API URL
   ```

### Docker Installation (Optional)
If you prefer using Docker, you can build and run the container:
```bash
docker build -t openhands-monitor .
```

## Usage

### Running the Bot

#### Method 1: Direct Python execution (Recommended for development)
```bash
python bot.py
```

#### Method 2: Using Docker Compose (Recommended for production)
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

### What to Expect
Once running, the bot will:
1. Send a startup notification to Telegram: "🤖 OpenHands Monitor Bot is online and starting to poll."
2. Begin polling the OpenHands API every 5 seconds
3. Send notifications for:
   - New tasks started
   - Task status changes
   - Task completions

## Configuration

### Required Environment Variables

The bot requires the following environment variables to be set. These can be configured in a `.env` file in the project root or set directly in your environment.

| Variable | Description | Required | Default Value | Example |
|----------|-------------|----------|---------------|---------|
| `TELEGRAM_TOKEN` | Your Telegram bot token obtained from [@BotFather](https://t.me/botfather) | **Yes** | None | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `CHAT_ID` | Telegram chat ID where notifications will be sent | **Yes** | None | `-1001234567890` |
| `OPENHANDS_API_URL` | OpenHands API base URL | No | `http://host.docker.internal:3000` | `http://localhost:3000` or `https://api.openhands.example.com` |

### Creating the `.env` File

Create a `.env` file in the project root directory with the following content:

```bash
# Required: Telegram Bot Token from @BotFather
TELEGRAM_TOKEN=your_telegram_bot_token_here

# Required: Telegram Chat ID for notifications
CHAT_ID=your_telegram_chat_id_here

# Optional: OpenHands API URL (defaults to http://host.docker.internal:3000)
OPENHANDS_API_URL=http://localhost:3000
```

### Obtaining Telegram Credentials

1. **Create a Telegram bot**:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Use `/newbot` command to create a new bot
   - Save the token provided by BotFather

2. **Get Chat ID**:
   - Add your bot to the desired chat/channel
   - Send any message to the bot
   - Use the following command to get updates (replace `<YOUR_TOKEN>`):
     ```bash
     curl "https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates"
     ```
   - Look for the `chat.id` field in the response

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

### Key Files Description

- **bot.py**: Main monitoring module that polls OpenHands API and sends Telegram notifications
- **map_maker.py**: Dictionary module for word definitions lookup
- **requirements.txt**: Python dependencies including `python-telegram-bot`, `httpx`, and `tenacity`
- **Dockerfile**: Container configuration for Docker deployment
- **docker-compose.yml**: Docker Compose configuration for easy orchestration

## Quick Start

### Installation and Setup in 5 Minutes

```bash
# 1. Clone the repository
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
# Create a .env file with:
# TELEGRAM_TOKEN=your_telegram_bot_token
# CHAT_ID=your_telegram_chat_id
# OPENHANDS_API_URL=http://localhost:3000

# 4. Run the bot
python bot.py
```

### Getting Telegram Credentials

1. **Create a Telegram bot** via [@BotFather](https://t.me/botfather)
2. **Get your Chat ID**:
   ```bash
   curl "https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates"
   ```