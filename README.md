# OpenHands Monitor Bot

A Telegram bot for monitoring OpenHands platform tasks and sending real-time notifications about task status changes.

## Overview

The OpenHands Monitor Bot is a real-time monitoring solution that tracks task status changes on the OpenHands platform and sends instant notifications via Telegram. It continuously polls the OpenHands API for conversation/task updates and alerts users about new tasks, status changes, and task completions.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/bughouse-wizzard/openhands-monitor-bot.git
cd openhands-monitor-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the `.env.example` file to `.env` and update it with your actual values:

```bash
cp .env.example .env
```

Edit the `.env` file to set the necessary environment variables:

## Usage

Run the bot with the following command:

```bash
python bot.py
```

## Configuration

### Required Environment Variables

Set the following environment variables in your `.env` file:

- `TELEGRAM_TOKEN`: Your Telegram bot token (obtained from [@BotFather](https://t.me/botfather))
- `CHAT_ID`: Telegram chat ID for notifications
- `OPENHANDS_API_URL`: OpenHands API base URL (default: `http://host.docker.internal:3000`)
