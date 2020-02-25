import logging
import os

import telegram
from celery import Celery
from dotenv import load_dotenv

from scraping_info import ScrapingInfo

load_dotenv()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
token = os.getenv("API_TOKEN")
channel = os.getenv("CHANNEL_NAME")

app = Celery('scraper')
app.conf.update(BROKER_URL=os.getenv("RABBITMQ_URL"))

bot = telegram.Bot(token=token)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@app.task
def matching_found(chat_id, web_page_url):
    bot.send_message(chat_id=chat_id,
                     text=f"Found matching at {web_page_url}")
