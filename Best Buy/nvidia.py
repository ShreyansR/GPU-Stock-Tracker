from bs4 import BeautifulSoup as soup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import sys

from discord import Webhook, RequestsWebhookAdapter
import discord
import datetime
from dotenv import load_dotenv

load_dotenv()
PROXY = "64.235.204.107:8080"

my_url = 'https://www.canadacomputers.com/index.php?cPath=43&sf=:3_3,3_5,3_7,3_8,3_9&mfr=&pr=500-1000'
my_url2 = 'https://www.facebook.com/CanadaComputers/'
my_url3 = 'https://www.canadacomputers.com/index.php?cPath=43&sf=:2_1&mfr=&pr=50-74.99'
test_url = 'https://www.canadacomputers.com/search/results_details.php?language=en&keywords=Asus+GeForce+GT+1030+LP+2GB'

house_num = os.getenv('TEST_HOUSE_NUMBER')
street_name = os.getenv('TEST_STREET_NAME')
postal_code = os.getenv('TEST_POSTAL_CODE')

cholder_name = os.getenv('TEST_CHOLDER_NAME')
card_number = os.getenv('TEST_CARD_NUMBER')
card_expiry = os.getenv('TEST_CARD_EXPIRY')
card_ccv = os.getenv('TEST_CARD_CCV')

base_URL = "https://www.bestbuy.ca/en-ca/product/"
urls = ["https://www.bestbuy.ca/en-ca/product/zotac-nvidia-geforce-rtx-3080-ti-amp-holo-12gb-gddr6x-video-card/15507363",
        "https://www.bestbuy.ca/en-ca/product/asus-rog-strix-nvidia-geforce-rtx-3080-ti-oc-12gb-gddr6x-video-card/15493494",
        "https://www.bestbuy.ca/en-ca/product/msi-nvidia-geforce-rtx-3080-ti-ventus-3x-oc-12gb-gddr6-video-card/15524483",
        "https://www.bestbuy.ca/en-ca/product/msi-nvidia-geforce-rtx-3080-ti-gaming-x-trio-12gb-gddr6-video-card/15524484",
        "https://www.bestbuy.ca/en-ca/product/evga-geforce-rtx-3080-ti-ftw3-ultra-12gb-gddr6x-video-card/15524485",
        "https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3080-ti-12gb-gddr6x-video-card/15530045"]

urls2 = ["https://www.bestbuy.ca/en-ca/product/15530046",
        "https://www.bestbuy.ca/en-ca/product/15546964",
        "https://www.bestbuy.ca/en-ca/product/15545267",
        "https://www.bestbuy.ca/en-ca/product/15545266",
        "https://www.bestbuy.ca/en-ca/product/15547752",
        "https://www.bestbuy.ca/en-ca/product/15547753"]

# Initiate Webhook for Discord
def create_webhook():
    wHook = os.getenv('BESTBUY_WEBHOOK')
    webhook = Webhook.from_url(wHook, adapter=RequestsWebhookAdapter())
    return webhook

# Initiate Chrome Driver
def create_driver():
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument('--proxy-server=%s' % PROXY)
    driver = webdriver.Chrome(options=op)
    return driver

# Initiate Bot
def bot(driver, webhook):
    driver.maximize_window()                                                                                                   # Maximize chrome window, disable it if using chrome headless

    while 1:
        # Launch CC Website in the Login Page, Accept Cookies and Login
        for url in urls2:
            driver.get(url)
            #time.sleep(1)
            page_html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            page_soup = soup(page_html, "lxml")
            product = page_soup.find("h1", {"class": "productName_3nyxM"}).text.strip()
            cart_button = page_soup.find("div", {"class": "addToCartContainer_20u-G"})
            cart_class = ' '.join(cart_button.form.button['class'])
            price = page_soup.find("span", {"class": "screenReaderOnly_3anTj large_3aP7Z"}).text.strip()
            img_search = page_soup.find("img", {"class": "productImage_1NbKv"})
            img_url = img_search['src']
            #print(cart_class)

            if (cart_class == "button_2m0Gt primary_RXOwf addToCartButton_1op0t addToCartButton regular_23pTm disabled_LqxUL"):
                print(product, " Is Not Available")

            elif cart_class == "button_2m0Gt primary_RXOwf addToCartButton_1op0t addToCartButton regular_23pTm":
                print(product, " Is Available")

                # Send Discord Embed to Channel through Webhook
                e = discord.Embed(title=product, url=url)
                e.set_image(url=img_url)
                e.add_field(name="Product Link", value=url)
                e.add_field(name="Price", value=price)
                e.timestamp = datetime.datetime.utcnow()
                webhook.send(embed=e)
            time.sleep(1)
            # if driver.find_element_by_css_selector("button[class='button_E6SE9 primary_1oCqK addToCartButton_1op0t addToCartButton regular_1jnnf'"):
            #     print(driver.find_elements_by_class_name("productName_3nyxM").text.strip() + " Is Available")
            #
            # elif driver.find_elements_by_class_name()
        # driver.get('https://www.canadacomputers.com/login.php')
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "privacy-btn"))).click()
        # driver.find_element_by_id("lo-username").send_keys(os.getenv("CC_USERNAME"))
        # time.sleep(1)
        # driver.find_element_by_id("lo-password").send_keys(os.getenv("CC_PASS"))
        # time.sleep(1)
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btn-login"))).click()

        time.sleep(3)
                                                                                                               # Check for new products every 20 seconds


# Method for buying a card
def buy_card(driver, webhook, url, price):

    # Go to product page
    driver.get(url)

    # Get product page html and convert to soup and get product availability
    page_html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    page_soup = soup(page_html, "lxml")
    product_availability = page_soup.find("p", {"id": "storeinfo"})

    # Check if product is available
    if (product_availability.text.strip() != "Out of stockat (All Locations)NO AVAILABLE items ONLINE"):

        # Get the locations the product is available at
        product_location = page_soup.find("p", {"id": "asofinfo"})

        # Check if product is available in any preferred locations and add to cart if true
        if (product_location.text.strip() == "at Midtown Toronto, ON"
            or product_location.text.strip() == "at Mississauga, ON"
            or product_location.text.strip() == "at Midtown Toronto, ON"
            or product_location.text.strip() == "at ONLINE"
            or product_location.text.strip() == "at Etobicoke, ON"
            or product_location.text.strip() == "at Oakville, ON"
            or product_location.text.strip() == "at Burlington, ON"
            or product_location.text.strip() == "at Hamilton, ON"
            or product_location.text.strip() == "at Markham, ON"
            or product_location.text.strip() == "at Scarborough, ON"
            or product_location.text.strip() == "at Vaughan, ON"
            or product_location.text.strip() == "at Whitby, ON"
            or product_location.text.strip() == "at Oshawa, ON"
            or product_location.text.strip() == "at North York, ON"
            or product_location.text.strip() == "at Ajax, ON"
            or product_location.text.strip() == "at Brampton, ON"
            or product_location.text.strip() == "at Richmond Hill, ON"
            or product_location.text.strip() == "at Downtown Toronto, ON"
            or product_location.text.strip() == "at Waterloo, ON"
            or product_location.text.strip() == ""):

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "btn-addCart")))
                driver.find_element_by_id("btn-addCart").click()
                time.sleep(5)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "btn-checkout")))
                driver.find_element_by_id("btn-checkout").click()
                time.sleep(2)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "lo-username")))
                driver.find_element_by_id("lo-username").send_keys(os.getenv("CC_USERNAME"))
                time.sleep(1)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "lo-password")))
                driver.find_element_by_id("lo-password").send_keys(os.getenv("CC_PASS"))
                time.sleep(1)
                driver.find_element_by_id("cm-btn-login").click()
                time.sleep(2)
            except:
                print("Card no longer available")
                webhook.send("Card no longer available")
                return

            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#cart > div > div.col-lg-3.col-md-4.pt-2.pt-md-0 > div > h2:nth-child(7) > strong > span")))
            # Check if product price is same as checkout price (This prevents from checking out with unwanted products in the cart)
            if driver.find_element_by_css_selector("#cart > div > div.col-lg-3.col-md-4.pt-2.pt-md-0 > div > h2:nth-child(7) > strong > span").text.strip() == price:

                # Click Proceed to Checkout button
                WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn bg-green text-white font-1 text-center f-500 py-1']")))
                driver.find_element_by_css_selector("button[class='btn bg-green text-white font-1 text-center f-500 py-1']").click()
                time.sleep(2)

                WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/form/div[1]/div[1]/div[1]/div[1]/input")))
                # Check if online purchase is enabled and initiate the purchase if True
                if driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/div[1]/div[1]/div[1]/div[1]/input").is_enabled():
                    online_purchase(driver, webhook)
                    return

                # If online purchase is disabled and only in store pick up is available, initiate the purchase if True
                if (driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/div[1]/div[1]/div[1]/div[1]/input").is_enabled() == False
                        and driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/div[1]/div[1]/div[1]/div[2]/input").is_enabled()):

                    store_pickup(driver, webhook)
                    return

        # If product not available in preferred stores
        else:
            webhook.send("Card not available online or in preferred stores")

# Method for online purchase
def online_purchase(driver, webhook):

    # Try to start the checkout process
    try:
        # Checkout Shipping
        print("Checkout shipping")
        driver.find_element_by_name("checkout_shipping").send_keys(Keys.ENTER)
        time.sleep(10)

        # Checkout Shipping Options
        print("Checkout Shipping Option")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/form/div[3]/div/button[2]"))).click()

        # Payment Method
        print("Checkout Payment")
        driver.find_element_by_name("checkout_payment").send_keys(Keys.ENTER)
        time.sleep(5)

        # Confirm/Review Checkout
        print("Checkout confirmation")
        driver.find_element_by_name("checkout_confirmation").send_keys(Keys.ENTER)
        time.sleep(2)

        # Enter Payment Details
        print("Entering Card Details")
        driver.find_element_by_xpath("/html/body/div[1]/main/div/div[4]/div[3]/div[2]/p[1]/input").send_keys(house_num)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[1]/main/div/div[4]/div[3]/div[2]/p[2]/input").send_keys(street_name)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[1]/main/div/div[4]/div[3]/p[3]/input").send_keys(postal_code)
        time.sleep(1)

        driver.find_element_by_xpath("/html/body/div[1]/main/div/div[4]/div[3]/div[7]/p[1]/input").send_keys(cholder_name)
        #time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[1]/main/div/div[4]/div[3]/div[7]/p[2]/input").send_keys(card_number)
        #time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[1]/main/div/div[4]/div[3]/div[7]/p[3]/input").send_keys(card_expiry)
        #time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[1]/main/div/div[4]/div[3]/div[7]/p[4]/input").send_keys(card_ccv)
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[1]/main/div/div[4]/div[3]/div[10]/div[1]/input").click()
        time.sleep(5)

        if driver.find_element_by_id('error_box'):
            print("Card Purchase Error")
            sys.exit()

        else:
            print("Card Purchased")
            sys.exit()
        #sys.exit()

    except:
        #webhook.send("Card Purchase Failed")
        #clear_cart()
        sys.exit()


def store_pickup(driver, webhook):

    try:
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/div[1]/div[1]/div[1]/div[2]/input").click()
        page_html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        page_soup = soup(page_html, "lxml")
        locations = page_soup.findAll("div", {"class": "col-sm-4"})

        for location in locations:
            if (location.div.input['data-store-name'] == "Mississauga"
                    or location.div.input['data-store-name'] == "Midtown Toronto"
                    or location.div.input['data-store-name'] == "Etobicoke"
                    or location.div.input['data-store-name'] == "Oakville"
                    or location.div.input['data-store-name'] == "Burlington"
                    or location.div.input['data-store-name'] == "Hamilton"
                    or location.div.input['data-store-name'] == "Markham"
                    or location.div.input['data-store-name'] == "Scarborough"
                    or location.div.input['data-store-name'] == "Vaughan"
                    or location.div.input['data-store-name'] == "Whitby"
                    or location.div.input['data-store-name'] == "Oshawa"
                    or location.div.input['data-store-name'] == "North York"
                    or location.div.input['data-store-name'] == "Ajax"
                    or location.div.input['data-store-name'] == "Brampton"
                    or location.div.input['data-store-name'] == "Richmond Hill"
                    or location.div.input['data-store-name'] == "Downtown Toronto"
                    or location.div.input['data-store-name'] == "Waterloo"
                    or location.div.input['data-store-name'] == ""):
                print(location.div.input['data-store-name'])
                driver.find_element_by_id(location.div.input['id']).click()
                time.sleep(1)

                driver.find_element_by_name("checkout_shipping").send_keys(Keys.ENTER)
                time.sleep(10)
                driver.find_element_by_name("checkout_payment").send_keys(Keys.ENTER)
                time.sleep(10)
                # ACTIVATE CHECKOUT BY REMOVING THE COMMENTS BELOW
                # driver.find_element_by_name("checkout_confirmation").send_keys(Keys.ENTER)
                # time.sleep(2)
                webhook.send("Card Purchased")
                sys.exit()

    except:
        print("Card Purchase Failed")


def clear_cart():
    driver.get('https://www.canadacomputers.com/shopping_cart.php')
    if driver.find_element_by_css_selector("a[class='box-btn text-white my-1 btn_update_cart_quick']"):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='box-btn text-white my-1 btn_update_cart_quick']"))).click()

if __name__ == '__main__':
    driver = create_driver()
    webhook = create_webhook()
    bot(driver, webhook)
