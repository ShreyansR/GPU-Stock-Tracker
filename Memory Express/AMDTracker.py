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
import datetime
import requests

from discord import Webhook, RequestsWebhookAdapter
from dotenv import load_dotenv
load_dotenv()

my_url = 'https://www.memoryexpress.com/Category/VideoCards?FilterID=9e2f9741-d6ab-0ba6-06e1-440049798e7e'
my_url2 = 'https://www.memoryexpress.com/Category/VideoCards?FilterID=877021ae-b00f-e9d6-b67b-0f7d7419e503&PageSize=120'
base_url = 'https://www.memoryexpress.com'
image_base_url = 'https://media.memoryexpress.com/Images'
urls = []

def create_webhook():
    wHook = os.getenv('AMD_WEBHOOK_ME')
    webhook = Webhook.from_url(wHook, adapter=RequestsWebhookAdapter())
    return webhook

def create_driver():
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    return driver



def bot(driver, webhook):
    while 1:

        driver.get(my_url)

        page_html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        page_soup = soup(page_html, "lxml")

        product_list = page_soup.findAll("div", {"class": "c-shca-icon-item"})
        print(len(product_list), end='\n\n')

        for product in product_list:
            link = base_url + product.a['href']
            urls.append(link)

            imageURL = image_base_url + product.a['href']

            nameSearch = product.find("div", {"class": "c-shca-icon-item__body-name"})
            productName = nameSearch.a.text.strip()
            #print(productName)

            summary = product.find("div", {"class": "c-shca-icon-item__summary"})
            productPrice = (summary.div.div.span).text.strip()
            #print(productPrice)

            availability = product.find("div", {"class": "c-shca-icon-item__summary-actions"})
            #print(availability.a['class'])

            # if (' '.join(availability.a['class']) == 'c-shca-add-product-button c-shca-icon-item__summary-buy c-shca-icon-item__summary-buy--hidden'):
            #     print("Not available", end='\n\n')

            if (' '.join(availability.a['class']) == 'c-shca-add-product-button c-shca-icon-item__summary-buy'):
                e = discord.Embed(title=productName, url=link)
                e.set_image(url=imageURL)
                e.add_field(name="Product Link", value=link)
                e.add_field(name="Price", value=productPrice)
                e.timestamp = datetime.datetime.utcnow()
                webhook.send(embed=e)
                #webhook.send(product.a['href'])
                print("Available", end='\n\n')

        time.sleep(1800)
        driver.refresh()


if __name__ == '__main__':
    driver = create_driver()
    webhook = create_webhook()
    bot(driver, webhook)



