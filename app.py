import re
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from io import BytesIO

# Replace with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = '7615742646:AAFhMMzt978vsaL64Zcr1Fh06WYz1TJM9V4'

# Set up the request URL and headers
url = 'https://www.blackbox.ai/api/chat'
headers = {
    'authority': 'www.blackbox.ai',
    'accept': '*/*',
    'accept-language': 'en-SG,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'cookie': 'sessionId=21b9cdf9-df30-486f-b114-0d34c05b5c42; __Host-authjs.csrf-token=...',
    'origin': 'https://www.blackbox.ai',
    'referer': 'https://www.blackbox.ai/agent/ImageGenerationLV45LJp',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

# Dictionary to keep track of users who have started the bot
user_started = {}

# Define the /start command handler
def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    user_started[user_id] = True
    update.message.reply_text("Welcome! Please enter your text to generate an image.")

# Define the message handler for generating images
def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    
    # Check if the user has used /start
    if user_started.get(user_id):
        # Get user message content
        user_content = update.message.text

        # Set up the data payload with dynamic content input
        data = {
            "messages": [
                {"id": "user-message", "content": user_content, "role": "user"}
            ],
            "id": "unique-id",
            "previewToken": None,
            "userId": None,
            "codeModelMode": True,
            "agentMode": {"mode": True, "id": "ImageGenerationLV45LJp", "name": "Image Generation"},
            "trendingAgentMode": {},
            "isMicMode": False,
            "maxTokens": 1024,
            "playgroundTopP": None,
            "playgroundTemperature": None,
            "isChromeExt": False,
            "githubToken": None,
            "clickedAnswer2": False,
            "clickedAnswer3": False,
            "clickedForceWebSearch": False,
            "visitFromDelta": False,
            "mobileClient": False,
            "userSelectedModel": None
        }

        # Send the request
        response = requests.post(url, headers=headers, json=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Use regex to extract the image URL
            match = re.search(r'https://storage\.googleapis\.com/[^\s\)]+', response.text)
            if match:
                image_url = match.group(0)
                # Download the image
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    # Send the image as a file to the user
                    image_file = BytesIO(image_response.content)
                    image_file.name = 'generated_image.jpg'
                    update.message.reply_photo(photo=image_file)
                else:
                    update.message.reply_text("Failed to download the image.")
            else:
                update.message.reply_text("Could not find an image URL in the response.")
        else:
            update.message.reply_text("An error occurred with the API request.")
    else:
        # If user hasn't started the bot, prompt them to do so
        update.message.reply_text("Please use /start first to begin.")

# Define the main function to set up the bot
def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(TELEGRAM_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the command handler for /start
    dispatcher.add_handler(CommandHandler('start', start))
    
    # Register the message handler for generating images
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process is terminated
    updater.idle()

if __name__ == '__main__':
    main()
