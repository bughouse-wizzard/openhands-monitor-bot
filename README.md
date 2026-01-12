# OpenHands Monitor Bot

A Telegram bot for monitoring OpenHands platform tasks and sending real-time notifications about task status changes.

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

Create a `.env` file in the project root with the necessary environment variables:

```bash
TELEGRAM_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
OPENHANDS_API_URL=http://localhost:3000
```

## Usage

Run the bot with the following command:

```bash
python bot.py
```

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

