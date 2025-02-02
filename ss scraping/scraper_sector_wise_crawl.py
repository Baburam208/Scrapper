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

# Wait for the dropdown to load
dropdown_element = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, 'sector'))
)

# Text for the desired option (this can be changed dynamically)
"""
1. Commercial Bank
2. Development Bank
3. Finance
4. Hotel & Tourism
5. Hydropower
6. Investment
7. Life Insurance
8. Manufacturing and Processing
9. Microfinance
10. Non-Life Insurance
11. Others
12. Trading
"""
sector_name = "Commercial Bank"  # Change this to "Development Bank", "Finance", etc.

os.makedirs(sector_name, exist_ok=True)

# Scroll the dropdown into view
browser.execute_script("arguments[0].scrollIntoView(true);", dropdown_element)

# Use JavaScript to directly click the option by the desired visible text
browser.execute_script("""
    let selectElement = arguments[0];
    let options = selectElement.querySelectorAll('option');
    let desiredOptionText = arguments[1];
    let desiredOption = Array.from(options).find(option => option.text === desiredOptionText);
    if (desiredOption) {
        desiredOption.selected = true;
        selectElement.dispatchEvent(new Event('change'));
    }
""", dropdown_element, sector_name)

# sdate = date(YYYY, MM, DD)  # Replace YYYY, MM, DD with the actual start date
# edate = date(YYYY, MM, DD)  # Replace YYYY, MM, DD with the actual end date

sdate = date(2012, 1, 1)  # Replace YYYY, MM, DD with the actual start date
edate = date(2025, 1, 20)  # Replace YYYY, MM, DD with the actual end date

dates = return_dates(sdate, edate)

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
    scrape_table(data=html, date=day, sector=sector_name)

# Close the browser
browser.quit()
