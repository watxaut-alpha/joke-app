from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging

from src.bot.secret import TOKEN
import src.bot.functions as bot


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger('jokeBot')

    # telegram bot init
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # adds the functions to the bot function
    dispatcher.add_handler(CommandHandler('start', bot.start))

    dispatcher.add_handler(CommandHandler('send_joke', bot.send_joke))

    dispatcher.add_handler(CommandHandler('rate_joke', bot.rate_joke))

    dispatcher.add_handler(CommandHandler('validate_joke', bot.validate_joke))

    # button rating
    dispatcher.add_handler(CallbackQueryHandler(bot.button_rating))

    logger.info('--- Starting bot ---')

    # starts receiving calls
    updater.start_polling(timeout=10)
    updater.idle()

