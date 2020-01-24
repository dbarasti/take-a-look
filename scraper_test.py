import requests
from bs4 import BeautifulSoup

propaganda_url = "https://www.la7.it/registrazioni/registrazioni-propaganda"
iframe_link = "https://d2b813qtup3hez.cloudfront.net/template/elenco.html"
element = "div"
attribute = "class"
value = "data_ora-content"
regex_pattern = "27-01-2020"

response = requests.get(propaganda_url)
soup = BeautifulSoup(response.text, "html.parser")
frames = soup.findAll("iframe")
for frame in frames:
    print(frame["src"])

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
