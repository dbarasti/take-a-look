import os
import re
import time

import requests
import schedule
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

web_page_url = "https://www.asos.com/it/asos-design/asos-design-risparmia-con-confezione-da-5-paia-di-calzini-sportivi-bianchi/prd/12271458?CTAref=Complete+the+Look+Carousel_2&featureref1=complete+the+look"
# web_page_url = "https://www.la7.it/registrazioni/registrazioni-propaganda"
# element = "div"
tag = "div"
attribute = "class"
# attribute = "class"
value = "product-hero"
# value = "data_ora-content"
regex_pattern = "ESAURITO"
# regex_pattern = "(0*(?:[1-9][0-9]?|200))"

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")
driver = webdriver.Chrome("/usr/bin/chromedriver")
driver.implicitly_wait(2)  # seconds


# regex_pattern = "27-01-2020"


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
                    matching_found()
                else:
                    print("not found")

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

        def matching_found():
            duration = 1  # seconds
            freq = 440  # Hz
            print(f"Found matching of {pattern} at {url}")
            os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

        response = make_request()
        elaborate_response()

    schedule.every(10).seconds.do(scrape_url, page_url)
    iframes = find_iframe_urls(page_url)
    for iframe in iframes:
        schedule.every(10).seconds.do(scrape_url, iframe)


scrape_page(web_page_url, regex_pattern)
schedule.run_all()
while True:
    schedule.run_pending()
    time.sleep(1)

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
