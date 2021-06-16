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

main_url = 'https://www.canadacomputers.com/index.php?cPath=43&sf=:3_3,3_4,3_5,3_6,3_7&mfr=&pr=500-2500'
my_url2 = 'https://www.facebook.com/CanadaComputers/'
my_url3 = 'https://www.canadacomputers.com/index.php?cPath=43&sf=:2_1&mfr=&pr=50-74.99'
test_url = 'https://www.canadacomputers.com/search/results_details.php?language=en&keywords=Asus+GeForce+GT+1030+LP+2GB'

house_num = os.getenv('HOUSE_NUMBER')
street_name = os.getenv('STREET_NAME')
postal_code = os.getenv('POSTAL_CODE')

first_name = os.getenv('FIRST_NAME')
last_name = os.getenv('LAST_NAME')
address = os.getenv('HOUSE_ADDRESS')

cholder_name = os.getenv('CHOLDER_NAME')
card_number = os.getenv('CARD_NUMBER')
card_expiry = os.getenv('CARD_EXPIRY')
card_ccv = os.getenv('CARD_CCV')

urls = []

# Initiate Webhook for Discord
def create_webhook():
    wHook = os.getenv('NVIDIA_WEBHOOK_CC')
    webhook = Webhook.from_url(wHook, adapter=RequestsWebhookAdapter())
    return webhook

# Initiate Chrome Driver
def create_driver():
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    return driver

# Initiate Bot
def bot(driver, webhook):
    #driver.maximize_window()                                                                                                   # Maximize chrome window, disable it if using chrome headless

    # Launch CC Website in the Login Page, Accept Cookies and Login
    driver.get('https://www.canadacomputers.com/login.php')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "privacy-btn"))).click()
    driver.find_element_by_id("lo-username").send_keys(os.getenv("CC_USERNAME"))
    time.sleep(1)
    driver.find_element_by_id("lo-password").send_keys(os.getenv("CC_PASS"))
    time.sleep(1)
    driver.find_element_by_id("btn-login").click()
    time.sleep(2)

    # Infinite loop to keep checking for available items
    while 1:
        pause = 2
        driver.get(main_url)
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down on the products page to load all items
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

        # Get products page html and convert to soup
        page_soup = soup(page_html, "lxml")

        # Get a list of products from the products page
        product_list = page_soup.findAll("div", {"class": "col-xl-3 col-lg-4 col-6 mt-0_5 px-0_5 toggleBox mb-1"})

        # If no products available, stop bot and notify discord channel
        if(len(product_list) == 0):
            webhook.send("Website not responding")
            sys.exit()

        print(len(product_list))

        # Loop through each product in the list
        for product in product_list:

            # Get all product information (Name, Price, Image, ImageURL, etc)
            bar = product.find("div", {"class": "col-12 allInfoSearch"})
            info = product.find("div", {"class": "col-12 productImageDesc"})
            nameSearch = info.find("div", {"class": "px-0 col-12 productInfoSearch pt-2"})
            priceSearch = nameSearch.find("span", {"class": "d-block mb-0 pq-hdr-product_price line-height"})
            name = nameSearch.span.text.strip()
            price = priceSearch.strong.text.strip()
            imageSearch = product.find("img", {"class": "pq-img-manu_logo align-self-center"})
            imageURL = imageSearch['src']

            # Check if product in stock
            stock = bar.find("div", {"class": "mt-auto"})
            button = stock.find("button", {"class": "btn btn-primary text-center mb-1 mt-2 rounded-0 position-relative"})

            # If in stock, Add to Cart should be available
            if button.text.strip() == "Add to Cart":

                # Send Discord Embed to Channel through Webhook
                e = discord.Embed(title=name, url=product.a['href'])
                e.set_image(url=imageURL)
                e.add_field(name="Product Link", value=product.a['href'])
                e.add_field(name="Price", value=price)
                e.timestamp = datetime.datetime.utcnow()
                webhook.send(embed=e)

                # Initiate Card Buying Process
                #buy_card(driver, webhook, product.a['href'], price)
                time.sleep(1)
                #sys.exit()

            link = product.a['href']
            urls.append(link)

        time.sleep(20)
        driver.refresh()                                                                                                    # Check for new products every 20 seconds


# Method for buying a card
def buy_card(driver, webhook, url, price):

    # Go to product page
    driver.get(url)

    # Get product page html and convert to soup and get product availability
    page_html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    page_soup = soup(page_html, "lxml")
    product_availability = page_soup.find("p", {"id": "storeinfo"})

    # if(not driver.find_element_by_xpath("/html/body/header/div[1]/div/div[3]/div/div[4]/a/div/div")):
    #     return

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

            #WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#cart > div > div.col-lg-3.col-md-4.pt-2.pt-md-0 > div > h2:nth-child(7) > strong > span")))
            # Check if product price is same as checkout price (This prevents from checking out with unwanted products in the cart)
            if WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#cart > div > div.col-lg-3.col-md-4.pt-2.pt-md-0 > div > h2:nth-child(7) > strong > span"))).text.strip() == price:

                # Click Proceed to Checkout button
                WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn bg-green text-white font-1 text-center f-500 py-1']"))).click()
                time.sleep(2)

                # Check if online purchase is enabled and initiate the purchase if True
                if WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/form/div[1]/div[1]/div[1]/div[1]/input"))).is_enabled():
                    online_purchase(driver, webhook)
                    return

                # If online purchase is disabled and only in store pick up is available, initiate the purchase if True
                if (WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/form/div[1]/div[1]/div[1]/div[1]/input"))).is_enabled() == False
                        and (WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/form/div[1]/div[1]/div[1]/div[2]/input")))).is_enabled()):

                    store_pickup(driver, webhook)
                    return

        # If product not available in preferred stores
        else:
            webhook.send("Card not available online or in preferred stores")

# Method for online purchase
def online_purchase(driver, webhook):
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.NAME, "checkout_shipping")))
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
        time.sleep(2)

        if driver.find_element_by_id('error_box'):
            webhook.send("Card Purchase Error")
        else:
            webhook.send("Card Purchased")
        sys.exit()

    except:
        webhook.send("Card Purchase Failed")


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

                try:
                    driver.find_element_by_id("ch-frm-paymentcontact-verify-firstname").send_keys(first_name)
                    driver.find_element_by_id("ch-frm-paymentcontact-verify-lastname").send_keys(last_name)
                    driver.find_element_by_id("ch-frm-paymentcontact-verify-address-autocomplete").send_keys(address)
                    time.sleep(1)
                    driver.find_element_by_class_name("pac-item").click()
                    time.sleep(1)

                except:

                    driver.find_element_by_name("checkout_payment").send_keys(Keys.ENTER)
                    time.sleep(10)
                    # ACTIVATE CHECKOUT BY REMOVING THE COMMENTS BELOW
                    driver.find_element_by_name("checkout_confirmation").send_keys(Keys.ENTER)
                    time.sleep(2)
                    webhook.send("Card Purchased")
                    sys.exit()
    except:
        webhook.send("Card Purchase Failed")


def clear_cart():
    driver.get('https://www.canadacomputers.com/shopping_cart.php')
    if driver.find_element_by_css_selector("a[class='box-btn text-white my-1 btn_update_cart_quick']"):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='box-btn text-white my-1 btn_update_cart_quick']"))).click()


if __name__ == '__main__':
    driver = create_driver()
    webhook = create_webhook()
    bot(driver, webhook)
