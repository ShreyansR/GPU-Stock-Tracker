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
from itertools import cycle
from discord import Webhook, RequestsWebhookAdapter
from dotenv import load_dotenv
from lxml.html import fromstring
import random

brave_path = "C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe"
#
proxies = ['47.116.76.219:80']
proxy_pool = cycle(proxies)

my_url = 'https://www.canadacomputers.com/index.php?cPath=43&sf=:3_3,3_5,3_7,3_8,3_9&mfr=&pr='
my_url2 = 'https://www.canadacomputers.com/index.php?cPath=43'
urls = []

op = webdriver.ChromeOptions()
#op.add_argument('headless')
op.add_argument('--proxy-server=%s' % '35.203.60.138:8080')
driver = webdriver.Chrome(options=op)

pause = 0.5
driver.get(my_url2)
last_height = driver.execute_script("return document.body.scrollHeight")