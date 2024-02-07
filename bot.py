from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from selenium import webdriver
import threading
import time
import os

# Global variable to track whether the bot is currently fetching updates
is_fetching_updates = False

# Lock to prevent multiple threads from fetching updates simultaneously
fetch_updates_lock = threading.Lock()

# Path to the directory containing the ChromeDriver executable
chrome_driver_dir = os.path.join(os.getcwd(), 'chromedriver')

# Initialize Telegram Bot
bot_token = 'YOUR_BOT_TOKEN'
updater = Updater(token=bot_token)
dispatcher = updater.dispatcher

# Function to handle messages
def handle_message(update, context):
    global is_fetching_updates

    # Extract the message text
    message_text = update.message.text
    
    # Check if the bot is currently fetching updates
    if is_fetching_updates:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Another instance of the bot is currently processing updates. Please try again later.")
        return

    # Acquire the lock to prevent other threads from fetching updates
    with fetch_updates_lock:
        is_fetching_updates = True

        try:
            # Check if the message contains a URL
            if message_text.startswith('http://') or message_text.startswith('https://'):
                # Initialize Chrome webdriver in headless mode
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                driver = webdriver.Chrome(executable_path=chrome_driver_dir, options=options)

                # Open the webpage
                driver.get(message_text)

                # Find the element by ID
                coupon_element = driver.find_element_by_id("couponDigits2")

                # Add a delay
                time.sleep(1)

                # Get the text value
                coupon_code = coupon_element.text

                # Print the coupon code
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Coupon Code: {coupon_code}")

                # Create the new URL with coupon code
                new_url = message_text.replace("studybullet.com", "www.udemy.com") + f"?couponCode={coupon_code}"

                # Open the new URL
                driver.get(new_url)

                context.bot.send_message(chat_id=update.effective_chat.id, text=f"New URL: {new_url}")

                # Close the browser
                driver.quit()

        except Exception as e:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"An error occurred: {e}")

        finally:
            # Release the lock after processing updates
            is_fetching_updates = False

# Handler for starting the bot
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Bot is running. Send a URL to extract coupon code and generate a new link.')

# Add handlers to the dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

# Start the bot
updater.start_polling()
updater.idle()
