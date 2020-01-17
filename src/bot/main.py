import logging
import os

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

import src.functions as functions


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

# telegram bot init
TOKEN = os.getenv("TOKEN")
logger.info(f"TOKEN: {TOKEN}")
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# adds the functions to the bot function
dispatcher.add_handler(CommandHandler("start", functions.start))
dispatcher.add_handler(CommandHandler("send_joke", functions.send_joke))
dispatcher.add_handler(CommandHandler("rate_joke", functions.rate_joke))
dispatcher.add_handler(CommandHandler("validate_joke", functions.validate_joke))
dispatcher.add_handler(CommandHandler("tag_joke", functions.tag_joke))

# button rating
dispatcher.add_handler(CallbackQueryHandler(functions.button_rating))

logger.info("--- Starting bot ---")

# starts receiving calls
updater.start_polling(timeout=10)
updater.idle()
