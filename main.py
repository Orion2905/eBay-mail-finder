import array
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import messagebox, simpledialog, filedialog

import time
import os
import urllib.request
import pyperclip
import tkinter as tk
import random
import json
import datetime
from dateutil import parser
import locale

import mysql.connector
import random


#from bots.amazon.database import Database

class EbayEmailBot:
    def __init__(self):
        self.MAIN_URL = "https://www.ebay.it/"
        

        # self.db = Database()

        import os
        os.environ['GH_TOKEN'] = "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"

        driver = GeckoDriverManager().install()
        service = Service(driver)
        self.driver = webdriver.Firefox(
            service=service
        )

        self.actions = ActionChains(self.driver)

    def calculate_loading_time(self, url):
        try:
            random_delay = random.randint(1, 3)
            stream = urllib.request.urlopen(url)
            start_time = time.time()
            output = stream.read()
            end_time = time.time()
            stream.close()
            time_delay = end_time - start_time
            print(
                f"Delay time: {time_delay}; \nRandom Delay: {random_delay}; \nTotal Delay {time_delay + random_delay}"
            )
        except:
            random_delay = random.randint(1, 5)
            time_delay = 1
            print(
                f"Delay time: {time_delay}; \nRandom Delay: {random_delay}; \nTotal Delay {time_delay + random_delay}"
            )

        return time_delay + random_delay

    def close_browser(self):
        self.driver.close()
        messagebox.showinfo(title="Info", message="Process finished!")

    def get_url(self, url):
        self.driver.get(url)
        time.sleep(self.calculate_loading_time(url))

    def open_url_new_page(self, url):
        time.sleep(2)
        self.driver.execute_script(f'''window.open("{url}","_blank");''')
        test = self.driver.window_handles[1]
        self.driver.switch_to.window(test)

    def accept_cookies(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, "#gdpr-banner-accept").click()
        except:
            print("Pagina No Cookies")

    def scroll_down(self, page_number):
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        time_to_scroll = int(page_number)
        for i in range(time_to_scroll):
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(4)

            self.driver.find_elements(By.CSS_SELECTOR, ".a-button-input")[-1].click()
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_products(self):
        def seller_name():
            name = self.driver.find_element(By.CSS_SELECTOR, ".ux-seller-section__item--seller").text
            name = name.split(" ")[0]
            return name
        
        def seller_reviews():
            reviews = self.driver.find_element(By.CSS_SELECTOR, ".ux-seller-section__item--seller").text
            reviews = reviews.split(" ")[1].replace("(", "").replace(")", "")
            return reviews

        def seller_email():
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".ux-table-section--contactInformationDropdown .details__summary").click()
            except Exception as e:
                print(e)
            emails = self.driver.find_elements(By.CSS_SELECTOR, ".ux-textspans--HIGHLIGHT")
            email = emails[-1].text
            for i in range(len(emails)):
                if emails[i].text == "Email:":
                    email = emails[i+1].text
                    break
            return email

        def seller_phone():
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".ux-table-section--contactInformationDropdown .details__summary").click()
            except Exception as e:
                print(e)
            phones = self.driver.find_elements(By.CSS_SELECTOR, ".ux-textspans--HIGHLIGHT")
            phone = phones[-1].text
            for i in range(len(phones)):
                #print(phones[i].text)
                if phones[i].text == "Telefono:":
                    phone = phones[i+1].text
                    break
            return phone

        return {
            "Seller Name": seller_name(),
            "Seller Reviews": seller_reviews(),
            "Seller Email": seller_email(),
            "Seller Phone": seller_phone(),
        }
    
    def write_on_csv(self, product=[]):
        file_name = "contacts.csv"
        path = os.getcwd()
        file_list = os.listdir(path)
        if file_name not in file_list:
            with open(file_name, "w") as f:
                pass
        else:
            with open(file_name, "a") as f:
                f.write(f"{product['Seller Name']};{product['Seller Reviews']};{product['Seller Email']};{product['Seller Phone']}\n")

    def bot(self):
        url = "https://www.ebay.it/e/campagne-speciali/informatica-settembre23?rt=nc&LH_SellerWithStore=1"
        self.get_url(url)
        self.write_on_csv()
        for i in range(2, 10, 1):
            # Ottieni il numero di prodotti in quella pagina
            products = self.driver.find_elements(By.CSS_SELECTOR, '[class="s-item__info clearfix"]')
            for i in range(len(products)):
                product = products[i].get_attribute("innerHTML")
                product = product.split('href="')[1].split('"')[0]
                self.open_url_new_page(product)
                time.sleep(3)
                product = self.get_products()
                self.write_on_csv(product)
                time.sleep(2)
                self.driver.close()
                test2 = self.driver.window_handles[0]
                self.driver.switch_to.window(test2)
            
            self.get_url(url+"&_pgn="+str(i))








a = EbayEmailBot()
a.get_url(a.MAIN_URL)
a.accept_cookies()
a.bot()
a.close_browser()
