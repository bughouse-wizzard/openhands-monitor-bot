# OpenHands Monitor Bot

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

A Telegram bot for monitoring OpenHands platform tasks and sending real-time notifications about task status changes.

## Installation

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

## Usage

### Running the Bot

To start the bot, run:
```bash
python bot.py
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

| Variable | Description | Required | Default Value | Example |
|----------|-------------|----------|---------------|---------|
| `TELEGRAM_TOKEN` | Your Telegram bot token | Yes | None | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `CHAT_ID` | Telegram chat ID for notifications | Yes | None | `-1001234567890` |
| `OPENHANDS_API_URL` | OpenHands API base URL | No | `http://host.docker.internal:3000` | `http://localhost:3000` or `https://api.openhands.example.com` |

