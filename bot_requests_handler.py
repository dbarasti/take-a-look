import logging
import os
from multiprocessing.context import Process

from dotenv import load_dotenv
from selenium import webdriver
from telegram import (ReplyKeyboardRemove)
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.ext import (ConversationHandler)
from telegram.ext import Updater

from scraper import Scraper
from scraping_info import ScrapingInfo

load_dotenv()
token = os.getenv("API_TOKEN")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

URL, TAG, ATTRIBUTE, VALUE, REGEX = range(5)


def setup_driver():
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    option.add_argument(" — incognito")
    option.binary_location = os.getenv("GOOGLE_CHROME_SHIM")
    wd = webdriver.Chrome(chrome_options=option)
    wd.implicitly_wait(2)  # todo check if mandatory to do this
    return wd


def launch_scraper(driver, info: [ScrapingInfo]):
    scraper = Scraper(driver, info)
    scraper.run_scraping()


def start(update, context):
    update.message.reply_text(
        'Hi! I am ScraperBot. I will help you scrape the world. '
        'Send /cancel to stop talking to me.\n\n'
        'Which URL should I scrape for you?')

    return URL


def start_config(update, context):
    update.message.reply_text('I am now firing-up your configuration')
    context.chat_data['driver'] = setup_driver()
    context.chat_data['scraping-info'] = ScrapingInfo(update.message.chat_id, context.chat_data['url'],
                                                      context.chat_data['tag'],
                                                      context.chat_data['attribute'],
                                                      context.chat_data['value'],
                                                      context.chat_data['regex'])
    context.chat_data['process'] = Process(target=launch_scraper,
                                           args=(context.chat_data['driver'], [context.chat_data['scraping-info']],))
    context.chat_data['process'].start()


def stop_config(update, context):
    update.message.reply_text('Stopping your configuration')
    context.chat_data['process'].terminate()


def new_config(update, context):
    update.message.reply_text('Which URL should I scrape for you?')

    return URL


def url(update, context):
    user = update.message.from_user
    context.chat_data['url'] = update.message.text
    logger.info("URL of %s: %s", user.first_name, context.chat_data['url'])
    update.message.reply_text('Nice! Please send the html tag you wish to target')

    return TAG


def tag(update, context):
    user = update.message.from_user
    context.chat_data['tag'] = update.message.text
    logger.info("Tag of %s: %s", user.first_name, context.chat_data['tag'])
    update.message.reply_text('Gorgeous! Now, send me the attribute')

    return ATTRIBUTE


def attribute(update, context):
    user = update.message.from_user
    context.chat_data['attribute'] = update.message.text
    logger.info("Attribute of %s: %s", user.first_name, context.chat_data['attribute'])
    update.message.reply_text('Almost there. I need the value for the attribute')

    return VALUE


def value(update, context):
    user = update.message.from_user
    context.chat_data['value'] = update.message.text
    logger.info("Attribute Value of %s: %s", user.first_name, context.chat_data['value'])
    update.message.reply_text('Now the REGEX and that\'s it')

    return REGEX


def regex(update, context):
    user = update.message.from_user
    context.chat_data['regex'] = update.message.text
    logger.info("Regex of %s: %s", user.first_name, context.chat_data['regex'])
    update.message.reply_text('Thank you! Now I am ready to scrape the website. \n'
                              'Send the /runconfig command to run the configuration')

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('newconfig', new_config),
                      CommandHandler('runconfig', start_config),
                      CommandHandler('stopconfig', stop_config)],

        states={

            URL: [MessageHandler(Filters.text, url)],

            TAG: [MessageHandler(Filters.text, tag)],

            ATTRIBUTE: [MessageHandler(Filters.text, attribute)],

            VALUE: [MessageHandler(Filters.text, value)],

            REGEX: [MessageHandler(Filters.text, regex)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
