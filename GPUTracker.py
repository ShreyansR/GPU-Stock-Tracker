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
load_dotenv()

wHook = os.getenv('DISCORD_WEBHOOK')

def bot():
    webhook = Webhook.from_url(wHook, adapter=RequestsWebhookAdapter())
    my_url = 'https://www.canadacomputers.com/index.php?cPath=43&sf=:3_3,3_5,3_7,3_8,3_9&mfr=&pr='
    my_url2 = 'https://www.canadacomputers.com/index.php?cPath=43'
    urls = []

    op = webdriver.ChromeOptions()
    #op.add_argument('headless')
    driver = webdriver.Chrome(options=op)

    pause = 1
    driver.get(my_url)
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
        bar = product.find("div", {"class": "col-12 allInfoSearch"})
        info = product.find("div", {"class": "col-12 productImageDesc"})
        nameSearch = info.find("div", {"class": "px-0 col-12 productInfoSearch pt-2"})
        priceSearch = nameSearch.find("span", {"class": "d-block mb-0 pq-hdr-product_price line-height"})
        name = nameSearch.span.text.strip()
        price = priceSearch.strong.text.strip()
        stock = bar.find("div", {"class": "mt-auto"})
        button = stock.find("button", {"class": "btn btn-primary text-center mb-1 mt-2 rounded-0 position-relative"})

        #print(button.text.strip())
        if(button.text.strip() == "Add to Cart"):
            # print(product.a['href'])
            # print(price)
            e = discord.Embed(title=name, url=product.a['href'])
            e.add_field(name="Product Link", value=product.a['href'])
            e.add_field(name="Price", value=price)
            webhook.send(embed=e)
            #webhook.send(product.a['href'])


        link = product.a['href']
        urls.append(link)


schedule.every(0.2).minutes.do(bot)

while 1:
    schedule.run_pending()
    time.sleep(1)