import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

import os


def scrape_table(data, date, sector):

    # load data into bs4
    soup =BeautifulSoup(data, 'html.parser')
    # extract parts of  table from the page
    table = soup.find('table', { 'id': 'headFixed' })   
    # get the table headers
    headers = get_table_headers(table)

    os.makedirs('Common_date', exist_ok=True)
    
    # get all the rows of the table
    rows = get_table_rows(table)
    if len(rows) <2: 
        print("No record for ",date) 
        with open(f"Common_date/{sector}.txt", "a") as file:
            file.write(f"No record Found {date}\n")
        return 0
    # save table as csv file
    save_as_csv(headers, rows, date, sector)


def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    return [th.text.strip() for th in table.find("tr").find_all("th")]


def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find_all("tr")[1:]:
        # grab all td tags in this table row
        tds = tr.find_all("td")
        cells = [td.text.strip() for td in tds]
        rows.append(cells)
    return rows


def save_as_csv(headers,rows,date, sector):
    pd.DataFrame(rows, columns=headers).to_csv(f"{sector}/{date}.csv",index=False)
    print(date,"Saved")

    with open(f"Common_date/{sector}.txt", "a") as file:
            file.write(f"{date}\n")
    
    os.makedirs('Common_date', exist_ok=True)

    # Path to the CSV file
    csv_file = f'Common_date/{sector}.csv'

    # Check if the file exists
    file_exists = os.path.exists(csv_file)

    # Open the file in append mode
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the header if the file doesn't exist
        if not file_exists:
            writer.writerow(["date"])  # Column name
        # Append the date
        writer.writerow([date])
