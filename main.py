from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import re

GOOGLE_FORM = "https://forms.gle/dpqEQZFvYuigVHd9A"
ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"

#info from https://myhttpheader.com/
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(ZILLOW_URL, headers=headers)
page = response.text

soup = BeautifulSoup(page, "html.parser")

price_list = []
add_list = []

all_link_elements = soup.select(".StyledPropertyCardDataWrapper a")
link_list = [link["href"] for link in all_link_elements]

# print(soup.prettify())

prices = soup.find_all("span", {"class": "PropertyCardWrapper__StyledPriceLine"})

def clean_price(text):
    match = re.search(r'(\$\d,*\d{3})', text)
    return match.group(1) if match else None

for div in prices:
    price_list.append(clean_price(div.text))


addresss = soup.find_all("address", {"data-test": "property-card-addr"})

for add in addresss:
    no_space = add.text.replace('\n', '').lstrip(' ').rstrip(' ')
    nioce = no_space.rsplit('|', 1)
    if len(nioce) > 1:
        add_list.append(nioce[1])
    else:
        newp = nioce[0].split(", ", 1)
        add_list.append(newp[1])

for i in range(len(price_list)):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", value=True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(GOOGLE_FORM)

    time.sleep(2)

    addy = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    addy.send_keys(add_list[i])

    price = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(price_list[i])

    link = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(link_list[i])

    submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    submit_button.click()

    time.sleep(2)
    driver.quit()
