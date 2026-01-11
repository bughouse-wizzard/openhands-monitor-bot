# OpenHands Monitor Bot

A Telegram bot for monitoring OpenHands platform tasks and sending real-time notifications about task status changes.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
   cd openhands-monitor-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the `.env` file** with the necessary environment variables:
   Create a `.env` file in the project root with the following variables:
   ```bash
   TELEGRAM_TOKEN=your_telegram_bot_token
   CHAT_ID=your_telegram_chat_id
   OPENHANDS_API_URL=http://localhost:3000
   ```

## Usage

Run the bot with:
```bash
python bot.py
```

## Configuration

### Required Environment Variables

- `TELEGRAM_TOKEN`: Your Telegram bot token (required)
- `CHAT_ID`: Telegram chat ID for notifications (required)
- `OPENHANDS_API_URL`: OpenHands API base URL (optional, defaults to `http://host.docker.internal:3000`)