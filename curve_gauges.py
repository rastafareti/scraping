import lxml
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

links = []
titles = []

def find_proposals():

    html_text = requests.get('YOUR WEBSITE').text

    soup = BeautifulSoup(html_text, 'lxml')
    proposals = soup.find_all('span', class_ = 'link-top-line')

    for p in proposals:
        link_element = p.find('a', class_='title raw-link raw-topic-link')
        if link_element:
            link = link_element.get('href')
            title = link_element.text.strip()   

            #Append to lists
            links.append(link)
            titles.append(title)

            print(f"Link: {link}")
            print(f"Title: {title}")
            print(' ')

            



    def google_sheet():
        try:
            # Authenticate with Google Sheets
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name('YOUR JSON FILE', scope)
            client = gspread.authorize(creds)

            # Open the Google Sheet by its name
            sheet = client.open('CRV_Gauge_Proposals').sheet1

            # Append each link and title row by row
            for link, title in zip(links, titles):
                sheet.append_row([link, title])
            
            print("Data appended successfully!")
            
        except Exception as e:
            print(f"Error: {e}")

    google_sheet()

if __name__ == '__main__':
    days_to_run = 7  # example value; change to whatever you need
    for _ in range(days_to_run):
        find_proposals()
        time_wait = 4
        print(f"Waiting: {time_wait} hours...")
        time.sleep(21600)  # waits 4 hours
