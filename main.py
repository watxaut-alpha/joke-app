from telegram.ext import Updater, CommandHandler
import logging

from src.bot.secret import token
import src.bot.functions as bot


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger('jokeBot')

    # telegram bot init
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    # adds the functions to the bot
    dispatcher.add_handler(CommandHandler('start', bot.start))

    # adds send joke
    dispatcher.add_handler(CommandHandler('send_joke', bot.send_joke))

    logger.info('--- Starting bot ---')

    # starts receiving calls
    updater.start_polling(timeout=10)
    updater.idle()

