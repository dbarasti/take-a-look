from selenium import webdriver

from scraper import Scraper
from scraping_info import ScrapingInfo


def setup_driver():
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    option.add_argument(" — incognito")
    option.binary_location = '/usr/bin/google-chrome'
    wd = webdriver.Chrome(chrome_options=option, executable_path="/usr/bin/chromedriver")
    wd.implicitly_wait(2)  # todo check if mandatory to do this
    return wd


web_page_url_one = "https://www.amazon.it/dp/B07PVCVBN7/ref=gw_mso_comb_qc_tkl_it?pf_rd_p=35d27a20-fa53-42e7-a469-3002b616c2f2&pf_rd_r=T7W1AEHYX8P6SS7Z33MC"
web_page_url_two = "https://www.amazon.it/dp/B07FQ473ZZ/ref=gw_it_MSO_desk_eink_jg?pf_rd_p=7761484d-bb34-4390-975a-e54496eddd80&pf_rd_r=3R5WQ67Q47VXE12GZ1SA"
tag_g = "span"
attribute_g = "id"
value_g = "priceblock_ourprice"
regex_pattern_g = "(0*(?:[1-9][0-9]?|80))"

info_one = ScrapingInfo(web_page_url_one, tag_g, attribute_g, value_g, regex_pattern_g)
info_two = ScrapingInfo(web_page_url_two, tag_g, attribute_g, value_g, regex_pattern_g)
driver = setup_driver()
scraper = Scraper(driver, [info_one, info_two])
scraper.run_scraping()
