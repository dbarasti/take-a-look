from multiprocessing import Process

from selenium import webdriver

from scraper import Scraper
from scraping_info import ScrapingInfo


def setup_driver():
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    option.add_argument(" — incognito")
    option.binary_location = '/usr/bin/google-chrome'
    wd = webdriver.Chrome(chrome_options=option, executable_path="/usr/bin/chromedriver")
    wd.implicitly_wait(5)  # todo check if mandatory to do this
    return wd


web_page_url_one = "https://www.la7.it/registrazioni/registrazioni-propaganda"
web_page_url_two = "https://www.amazon.it/dp/B0758975BR/ref=gw_mso_comb_qc_rvd2_it?pf_rd_p=35d27a20-fa53-42e7-a469-3002b616c2f2&pf_rd_r=50X4EP3W5CVFC2XZB6BC"
tag_g = "div"
attribute_g = "class"
value_g = "data_ora-content"
# regex_pattern_g = "([5],\\d\\d\\d|\\d\\d,\\d{3,})"
regex_pattern_g = "10-04-2020"

info_one = ScrapingInfo(web_page_url_one, tag_g, attribute_g, value_g, regex_pattern_g)
info_two = ScrapingInfo(web_page_url_two, tag_g, attribute_g, value_g, regex_pattern_g)
driver_one = setup_driver()
# driver_two = setup_driver()


def launch_scraper(driver, info: [ScrapingInfo]):
    scraper = Scraper(driver, info)
    scraper.run_scraping()


p1 = Process(target=launch_scraper, args=(driver_one, [info_one],))
#p2 = Process(target=launch_scraper, args=(driver_two, [info_two, info_one],))

p1.start()
# p2.start()
p1.join()
# p2.join()