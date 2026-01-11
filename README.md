# OpenHands Monitor Bot

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

## Project Title & Description

A Telegram bot for monitoring OpenHands platform tasks and sending real-time notifications about task status changes. The bot continuously polls the OpenHands API for conversation/task updates and sends notifications to a configured Telegram chat when new tasks start or existing tasks change status.

## Installation

### Step-by-Step Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
   cd openhands-monitor-bot
   ```

2. **Install dependencies**:
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

Run the bot using the following command:

```bash
python bot.py
```

Once running, the bot will:
1. Send a startup notification to Telegram: "🤖 OpenHands Monitor Bot is online and starting to poll."
2. Begin polling the OpenHands API every 5 seconds
3. Send notifications for:
   - New tasks started
   - Task status changes
   - Task completions

## Configuration

### Required Environment Variables

The bot requires the following environment variables to be set:

| Variable | Description | Required | Default Value | Example |
|----------|-------------|----------|---------------|---------|
| `TELEGRAM_TOKEN` | Your Telegram bot token | Yes | None | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `CHAT_ID` | Telegram chat ID for notifications | Yes | None | `-1001234567890` |
| `OPENHANDS_API_URL` | OpenHands API base URL | No | `http://host.docker.internal:3000` | `http://localhost:3000` or `https://api.openhands.example.com` |

### Detailed Explanation of Environment Variables

#### TELEGRAM_TOKEN
- **Description**: The authentication token for your Telegram bot, obtained from [@BotFather](https://t.me/botfather)
- **How to obtain**: 
  1. Message [@BotFather](https://t.me/botfather) on Telegram
  2. Use the `/newbot` command to create a new bot
  3. Save the token provided by BotFather
- **Format**: Typically looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

#### CHAT_ID
- **Description**: The unique identifier of the Telegram chat where notifications will be sent
- **How to obtain**:
  1. Add your bot to the desired chat/channel
  2. Send any message to the bot
  3. Use the following command to get updates:
     ```bash
     curl "https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates"
     ```
  4. Look for the `chat.id` field in the response
- **Format**: Can be a positive number for private chats or a negative number for groups/channels

#### OPENHANDS_API_URL
- **Description**: The base URL of the OpenHands API that the bot will monitor
- **Default**: `http://host.docker.internal:3000` (for Docker containers)
- **Development**: Typically `http://localhost:3000` when running locally
- **Production**: Your production OpenHands API URL

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