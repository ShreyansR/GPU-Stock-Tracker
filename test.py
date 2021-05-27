import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import lxml
import schedule
import os
import discord
import requests

from discord import Webhook, RequestsWebhookAdapter
from dotenv import load_dotenv
from lxml.html import fromstring

load_dotenv()

wHook = os.getenv('DISCORD_WEBHOOK')

webhook = Webhook.from_url(wHook, adapter=RequestsWebhookAdapter())
my_url = 'https://www.canadacomputers.com/index.php?cPath=43&sf=:3_3,3_5,3_7,3_8,3_9&mfr=&pr='
my_url2 = 'https://www.canadacomputers.com/index.php?cPath=43'
urls = []

op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op)

pause = 0.5
driver.get(my_url2)
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(pause)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        #time.sleep(10)
        page_html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        break
    last_height = new_height

page_soup = soup(page_html, "lxml")
product_list = page_soup.findAll("div", {"class": "col-xl-3 col-lg-4 col-6 mt-0_5 px-0_5 toggleBox mb-1"})
print(len(product_list))

for product in product_list:
    link = product.a['href']
    urls.append(link)

print(urls)

for url in urls:
    driver.get(url)
    pHtml = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    pSoup = soup(pHtml, "lxml")
    toCartBtn = pSoup.findAll("div", {"class": "mb-0_5"})
    if (toCartBtn):
        print(url)

# schedule.every(0.2).minutes.do(bot)
#
# while 1:
#     schedule.run_pending()
#     time.sleep(1)