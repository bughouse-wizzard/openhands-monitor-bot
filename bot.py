import os
import docker
import telegram
from telegram.ext import Updater, CommandHandler

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
CONTAINER_NAME = os.environ.get('CONTAINER_NAME')

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()

    client = docker.from_env()
    container = client.containers.get(CONTAINER_NAME)

    for line in container.logs(stream=True):
        log_line = line.decode('utf-8').strip()
        if "AgentStateChanged" in log_line or "ERROR" in log_line or "Action" in log_line:
            updater.bot.send_message(chat_id=CHAT_ID, text=log_line)

if __name__ == '__main__':
    main()
