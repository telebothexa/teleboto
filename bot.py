from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from selenium import webdriver
import time

# Import your bot token from config.py
from config import BOT_TOKEN

# Path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\KY\Downloads\Compressed\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Initialize Telegram Bot
updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher

# Function to handle messages
def handle_message(update, context):
    # Extract the message text
    message_text = update.message.text

    # Check if the message is a forwarded message
    if update.message.forward_date:
        # Extract the forwarded message
        message_text = update.message.forward_from.text

    # Check if the message is lengthy
    if len(message_text) > 100:
        # Extract the URL if it contains 'https://studybullet.com/course/'
        urls = re.findall(r'https://studybullet\.com/course/[^\s]+', message_text)
        if urls:
            # Handle each URL found
            for url in urls:
                process_url(url, update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No valid URL found in the message.")
    else:
        # Check if the message contains a URL
        if message_text.startswith('http://') or message_text.startswith('https://'):
            process_url(message_text, update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No valid URL found in the message.")

# Function to process URL
def process_url(url, update, context):
    # Initialize Chrome webdriver
    driver = webdriver.Chrome(executable_path=chrome_driver_path)

    try:
        # Open the webpage
        driver.get(url)

        # Find the element by ID
        coupon_element = driver.find_element_by_id("couponDigits2")

        # Add a delay
        time.sleep(1)

        # Get the text value
        coupon_code = coupon_element.text

        # Print the coupon code
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Coupon Code: {coupon_code}")

        # Create the new URL with coupon code
        new_url = url.replace("studybullet.com", "www.udemy.com") + f"?couponCode={coupon_code}"

        # Open the new URL
        driver.get(new_url)

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"New URL: {new_url}")

    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

# Handler for starting the bot
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Bot is running. Send a URL to extract coupon code and generate a new link.')

# Add handlers to the dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

# Start the bot
updater.start_polling()
updater.idle()
