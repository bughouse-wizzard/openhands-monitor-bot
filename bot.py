import telebot
import docker
import os
import threading
import time

# Telegram Bot Configuration
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Docker Configuration
CONTAINER_NAME = "openhands-app"

bot = telebot.TeleBot(BOT_TOKEN)

def monitor_logs():
    client = docker.from_env()
    while True:
        try:
            container = client.containers.get(CONTAINER_NAME)
            for line in container.logs(stream=True, follow=True):
                log_line = line.decode("utf-8").strip()
                if "ERROR" in log_line:
                    bot.send_message(CHAT_ID, f"Error detected in {CONTAINER_NAME}: {log_line}")
        except docker.errors.NotFound:
            print(f"Container {CONTAINER_NAME} not found. Retrying in 60 seconds.")
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(60)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

if __name__ == "__main__":
    log_thread = threading.Thread(target=monitor_logs)
    log_thread.daemon = True
    log_thread.start()
    bot.polling()
