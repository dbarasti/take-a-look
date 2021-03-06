import json
import queue
import re
import threading
import time

import requests
import schedule
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from scraping_info import ScrapingInfo
from update_worker import matching_found


class Scraper:
    def __init__(self, driver: WebDriver, scraping_info: [ScrapingInfo]):
        self.driver = driver
        self.scraping_info = scraping_info
        self.job_queue = queue.Queue()
        self.results = {}

    @staticmethod
    def find_iframe_urls(from_url):
        iframes = []
        response = requests.get(from_url)
        soup = BeautifulSoup(response.text, "html.parser")
        frames = soup.findAll("iframe")
        for frame in frames:
            iframes.append(frame["src"])
        return iframes

    def run_scraping(self):
        def scrape_url(scraping_target: ScrapingInfo):
            def elaborate_response():
                for element_text in response:
                    res = re.findall(scraping_target.regex_pattern, str(element_text))
                    if len(res) > 0 and (self.results.get(scraping_target.web_page_url) is not True):
                        self.results[scraping_target.web_page_url] = True
                        matching_found.delay(scraping_target.chat_id, scraping_target.web_page_url)
                    elif len(res) == 0:
                        print(f"pattern not found in {element_text}")
                if not response:
                    self.results[scraping_target.web_page_url] = False
                    print("element not found in page")

            def make_request():
                self.driver.get(scraping_target.web_page_url)
                timeout = 10
                try:
                    WebDriverWait(self.driver, timeout)
                except TimeoutException:
                    print("Timed out waiting for page to load")
                    # self.driver.quit()
                elements = self.driver.find_elements_by_xpath(
                    f"//{scraping_target.tag}[@{scraping_target.attribute}='{scraping_target.value}']")
                return [x.text for x in elements]

            response = make_request()
            elaborate_response()

        def worker_main():
            while 1:
                job_func, job_args = self.job_queue.get()
                job_func(job_args)
                self.job_queue.task_done()

        for info in self.scraping_info:
            schedule.every(10).seconds.do(self.job_queue.put, [scrape_url, info])
            iframes = self.find_iframe_urls(info.web_page_url)
            for iframe in iframes:
                schedule.every(10).seconds.do(self.job_queue.put, [scrape_url,
                                                                   ScrapingInfo(info.chat_id, iframe, info.tag,
                                                                                info.attribute,
                                                                                info.value, info.regex_pattern)])
        worker_thread = threading.Thread(target=worker_main)
        worker_thread.start()

        while 1:
            schedule.run_pending()
            time.sleep(1)
