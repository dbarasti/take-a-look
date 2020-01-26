import logging
import os
from time import sleep

import telegram
from celery import Celery

from dotenv import load_dotenv

app = Celery('scraper', broker='amqp://localhost')
load_dotenv()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
token = os.getenv("API_TOKEN")
channel = os.getenv("CHANNEL_NAME")
bot = telegram.Bot(token=token)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@app.task
def matching_found(url, pattern):
    duration = 1  # seconds
    freq = 440  # Hz
    print(f"Found matching for {pattern} at {url}")
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    bot.send_message(chat_id=channel, text=f"Found matching for {pattern} at {url}")
