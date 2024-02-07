from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from your_bot_script import start, handle_message

# Import your bot token from config.py
from config import BOT_TOKEN

# Initialize Telegram Bot
updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher

# Add handlers to the dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

# Start the bot
updater.start_polling()
updater.idle()
