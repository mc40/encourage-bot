import configparser
import logging

import telegram
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'

def is_alpha(word):
     try:
         return word.encode('ascii').isalpha()
     except:
         return False

def reply_handler(bot, update):
    text = update.message.text
    reply_text = "I don't know how to reply."
    first_text = text[0]
    print(text)
    print(is_alpha(first_text))
    if is_alpha(first_text):
        # handle for English
        reply_text = 'yes'
    else:
        # handle for Chinese
        reply_text = text[1] + '啦' if len(text)> 2 else '好啦'
    bot.send_message(chat_id=update.message.chat_id, text=reply_text)

# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    # Running server
    app.run(debug=True)