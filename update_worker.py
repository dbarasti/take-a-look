import logging
import os

import telegram
from celery import Celery
from dotenv import load_dotenv

from scraping_info import ScrapingInfo

app = Celery('scraper', broker='amqp://localhost')
load_dotenv()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
token = os.getenv("API_TOKEN")
channel = os.getenv("CHANNEL_NAME")
bot = telegram.Bot(token=token)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@app.task
def matching_found(chat_id, web_page_url):
    duration = 0.5  # seconds
    freq = 440  # Hz
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    bot.send_message(chat_id=chat_id,
                     text=f"Found matching at {web_page_url}")
