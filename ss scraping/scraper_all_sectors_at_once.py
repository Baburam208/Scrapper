import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import date
from scrape_table_all import scrape_table
from return_dates import return_dates

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Firefox()

# Open the link
browser.get("https://www.sharesansar.com/today-share-price")

# Select the type of data to scrape
# Select Commercial Bank
search_bar = browser.find_element(By.ID, 'sector')
search_bar.send_keys('Development Bank')


# sdate = date(YYYY, MM, DD)  # Replace YYYY, MM, DD with the actual start date
# edate = date(YYYY, MM, DD)  # Replace YYYY, MM, DD with the actual end date

sdate = date(2024, 12, 1)  # Replace YYYY, MM, DD with the actual start date
edate = date(2025, 1, 25)  # Replace YYYY, MM, DD with the actual end date
  
dates = return_dates(sdate, edate) 

os.makedirs("All Sectors", exist_ok=True)

for day in dates:
    # Enter the date
    date_box = browser.find_element(By.ID, 'fromdate')
    date_box.clear()
    date_box.send_keys(day)
    
    # Click Search
    search_button = browser.find_element(By.ID, 'btn_todayshareprice_submit')
    search_button.click()
    time.sleep(4)  # Needed for this site
    
    # Simulate pressing Enter after clicking the search button
    ActionChains(browser).send_keys(Keys.ENTER).perform()
    time.sleep(5)  # Wait for data to load
    
    # Scrape the table
    html = browser.page_source
    scrape_table(data=html, date=day, sector="All Sectors")

# Close the browser
browser.quit()
