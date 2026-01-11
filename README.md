# OpenHands Monitor Bot

A Telegram bot for monitoring OpenHands platform tasks and sending real-time notifications about task status changes.

## Features

- **Real-time Monitoring**: Continuously polls OpenHands API for conversation/task updates
- **Status Change Detection**: Identifies new tasks, status changes, and completed tasks
- **Telegram Notifications**: Sends instant notifications to configured Telegram chat
- **Retry Logic**: Implements automatic retry for failed Telegram API calls
- **State Tracking**: Maintains conversation state between polling cycles
- **Error Handling**: Graceful handling of API errors and network issues

## Installation

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (obtain from [@BotFather](https://t.me/botfather))
- Telegram Chat ID (where notifications will be sent)
- OpenHands API access

### Setup Steps

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

### Running the Bot

Start the monitoring bot with:
```bash
python bot.py
```

The bot will:
1. Validate configuration and environment variables
2. Send a startup notification to Telegram
3. Begin continuous polling of OpenHands API
4. Send notifications for detected changes

### Stopping the Bot

Press `Ctrl+C` to gracefully stop the bot. A shutdown message will be displayed.

## Configuration

### Environment Variables

All configuration is done through environment variables. You can set them in a `.env` file or export them in your shell.

#### Required Variables

- `TELEGRAM_TOKEN`: Your Telegram bot token (required)
  - **Purpose**: Authentication token for the Telegram Bot API
  - **How to obtain**: Create a bot using [@BotFather](https://t.me/botfather) on Telegram
  - **Format**: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
  - **Example**: `TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

- `CHAT_ID`: Telegram chat ID for notifications (required)
  - **Purpose**: Identifier of the chat where notifications will be sent
  - **Can be**: A user ID, group ID, or channel ID
  - **How to find**: Use @userinfobot on Telegram to find your chat ID
  - **Example**: `CHAT_ID=123456789`

#### Optional Variables

- `OPENHANDS_API_URL`: OpenHands API base URL
  - **Purpose**: Base URL for the OpenHands API endpoint
  - **Default**: `http://host.docker.internal:3000`
  - **Format**: `http://localhost:3000` or `https://api.openhands.example.com`
  - **Example**: `OPENHANDS_API_URL=http://localhost:3000`

### Polling Configuration

The polling interval is hardcoded in `bot.py` as `POLL_INTERVAL = 5` (seconds). You can modify this value in the source code if needed.

## Development

### Project Structure

- `bot.py` - Main application module with monitoring logic
- `requirements.txt` - Python dependencies
- `README.md` - This documentation file

### Code Style

- Follows PEP 8 guidelines
- Uses type hints for all function signatures
- Implements comprehensive error handling
- Includes Google-style docstrings for all functions

### Testing

To run tests (if available):
```bash
pytest tests/
```

## Troubleshooting

### Common Issues

1. **"TELEGRAM_TOKEN and CHAT_ID environment variables must be set."**
   - Ensure your `.env` file exists in the project root
   - Verify variable names are spelled correctly
   - Check that values are not empty

2. **Telegram API errors**
   - Verify your bot token is valid and active
   - Ensure the bot has been added to the chat
   - Check that the chat ID is correct

3. **OpenHands API connection issues**
   - Verify the API URL is correct
   - Ensure the OpenHands service is running
   - Check network connectivity

4. **Bot not sending notifications**
   - Check if conversations exist in OpenHands
   - Verify the bot has permission to access the API
   - Monitor logs for error messages

### Logs

The bot outputs logs to stdout with timestamps. Check these logs for debugging information.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.