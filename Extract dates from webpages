%%% This script requires an input of a csv file with a list of webpages
%%% The script will crawl each page, looking for a specified date pattern and output those dates for each page in a new csv file



import csv
import requests
from bs4 import BeautifulSoup
import re

def extract_date_from_webpage(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()

        date_pattern = r"([A-Z]{1}[a-z]+\s\d{1,2},\s\d{4})"
        date_matches = re.findall(date_pattern, text)
        date = date_matches[0] if date_matches else "Date not found"

        return date
    else:
        return "Failed to retrieve webpage. Error: " + str(response.status_code)

def extract_dates_from_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)

        output_rows = []
        for row in rows:
            if row:
                webpage_url = row[0].strip('\ufeff')  # Remove BOM from the URL
                extracted_date = extract_date_from_webpage(webpage_url)
                output_rows.append([webpage_url, extracted_date])

    with open(output_file, 'w', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(output_rows)

# Example usage
input_csv_file = r'C:\Users\...\Input.csv'  # Replace with the path to your input CSV file
output_csv_file = r'C:\Users\...\Output.csv'  # Replace with the desired output CSV file path
extract_dates_from_csv(input_csv_file, output_csv_file)
