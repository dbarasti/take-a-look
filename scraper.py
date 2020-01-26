import queue
import re
import threading
import time

import requests
import schedule
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from update_worker import matching_found

# web_page_url = "https://www.asos.com/it/asos-design/asos-design-risparmia-con-confezione-da-5-paia-di-calzini-sportivi-bianchi/prd/12271458?CTAref=Complete+the+Look+Carousel_2&featureref1=complete+the+look"
web_page_url = "https://www.amazon.it/dp/B07PVCVBN7/ref=gw_mso_comb_qc_tkl_it?pf_rd_p=35d27a20-fa53-42e7-a469-3002b616c2f2&pf_rd_r=T7W1AEHYX8P6SS7Z33MC"
# tag = "h1"
tag = "span"
# attribute = ""
attribute = "id"
value = "priceblock_ourprice"
# value = "title "
# regex_pattern = "ESAURITO"
regex_pattern = "(0*(?:[1-9][0-9]?|40))"
#regex_pattern = ""


def setup_driver():
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    option.add_argument(" — incognito")
    option.binary_location = '/usr/bin/google-chrome'
    wd = webdriver.Chrome(chrome_options=option, executable_path="/usr/bin/chromedriver")
    # driver = webdriver.Chrome("/usr/bin/chromedriver")
    wd.implicitly_wait(2)  # seconds
    return wd


def find_iframe_urls(from_url):
    iframes = []
    response = requests.get(from_url)
    soup = BeautifulSoup(response.text, "html.parser")
    frames = soup.findAll("iframe")
    for frame in frames:
        iframes.append(frame["src"])
    return iframes


def scrape_page(page_url, pattern):
    def scrape_url(url):
        def elaborate_response():
            for element_text in response:
                res = re.findall(pattern, str(element_text))
                if len(res) > 0:
                    matching_found.delay(url, pattern)
                else:
                    print("not found")
            if not response:
                print("element not found in page")

        def make_request():
            driver.get(url)
            timeout = 10
            try:
                WebDriverWait(driver, timeout)
            except TimeoutException:
                print("Timed out waiting for page to load")
                driver.quit()
            elements = driver.find_elements_by_xpath(f"//{tag}[@{attribute}='{value}']")
            return [x.text for x in elements]

        response = make_request()
        elaborate_response()

    schedule.every(10).seconds.do(job_queue.put, [scrape_url, page_url])
    iframes = find_iframe_urls(page_url)
    for iframe in iframes:
        schedule.every(5).seconds.do(job_queue.put, [scrape_url, iframe])


driver = setup_driver()
job_queue = queue.Queue()
scrape_page(web_page_url, regex_pattern)


def worker_main():
    while 1:
        job_func, job_args = job_queue.get()
        job_func(job_args)
        job_queue.task_done()


worker_thread = threading.Thread(target=worker_main)
worker_thread.start()

while 1:
    schedule.run_pending()
    time.sleep(1)
