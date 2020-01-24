import os
import re
from threading import Thread
from time import sleep
import logging
import requests
from bs4 import BeautifulSoup

# TODO make processes scheduled

web_page_url = "https://www.asos.com/it/asos-design/asos-design-vestito-lungo-plisse-verde-con-stampa-a-fiorellini/prd/13664615?clr=verde-a-fiorellini&colourWayId=16556056&SearchQuery=&cid=13508"
# web_page_url = "https://www.la7.it/registrazioni/registrazioni-propaganda"
# element = "div"
element = "span"
attribute = "class"
# attribute = "class"
value = "current-price"
# value = "data_ora-content"
regex_pattern = "52"
# regex_pattern = "27-01-2020"


def find_iframe_urls(from_url):
    iframes = []
    response = requests.get(from_url)
    soup = BeautifulSoup(response.text, "html.parser")
    frames = soup.findAll("iframe")
    for frame in frames:
        iframes.append(frame["src"])
    return iframes


def scrape_page(url, target_element, target_attr, target_value, pattern):
    def scrape_url(page_url):
        def scrape():
            logger = logging.getLogger("default logger")
            while True:
                response = requests.get(page_url)
                if (400 < response.status_code < 500) or (500 < response.status_code < 600):
                    logger.error(f"Error ({response.status_code}) while loading {response.request.url}")
                elif response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    events = soup.findAll(target_element, attrs={target_attr: target_value})
                    for event in events:
                        res = re.findall(pattern, str(event))
                        if len(res) > 0:
                            matching_found()
                sleep(10)

        def matching_found():
            duration = 1  # seconds
            freq = 440  # Hz
            logging.info(f"Found matching of {pattern} at {page_url}")
            os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

        print(f"Scraping url {page_url}")
        process_ref = Thread(target=scrape)
        process_ref.start()
        return process_ref
    scrape_url(url)
    iframes = find_iframe_urls(url)
    for iframe in iframes:
        scrape_url(iframe)


scrape_page(web_page_url, element, attribute, value, regex_pattern)

'''
driver = webdriver.Chrome("/usr/bin/chromedriver")
# driver.implicitly_wait(2)  # seconds
driver.get(propaganda_url)
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, 'spazioBannerSubHeader')))
# myDynamicElement = driver.find_element_by_id("accordion")
print(element)
'''

'''
f = open("output.html", "w")
f.write(driver.page_source)
# print(driver.page_source)
'''
