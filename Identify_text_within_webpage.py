# This script requires an input of a csv file with a list of webpages
%%% The script will crawl each page, looking for a specified keyword and output a 1 or 0 for each page in a new csv file, identifying which pages have one or more of those keywords



import csv
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re

async def fetch(session, url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    async with session.get(url, headers=headers, timeout=10) as response:
        content = await response.read()
        try:
            # Try decoding using UTF-8
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            # If decoding using UTF-8 fails, try decoding using ISO-8859-1 (Latin-1)
            text = content.decode('iso-8859-1')
        return text

async def check_phrases_in_webpage(session, url):
    try:
        html = await fetch(session, url)
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        return "Failed to retrieve webpage. Error: " + str(e)

    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text().lower()

    phrases_to_check = ["KEYWORD1" ,"KEYWORD2","KEYWORD3","KEYWORD4"]
    found = any(phrase in text for phrase in phrases_to_check)

    return "1" if found else "0"

async def check_phrases_for_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            await asyncio.sleep(2)  # Add a delay of 2 seconds between requests
            tasks.append(check_phrases_in_webpage(session, url))
        return await asyncio.gather(*tasks)

def check_phrases_in_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)

        urls = [row[0].strip('\ufeff') for row in rows if row]

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(check_phrases_for_urls(urls))

    with open(output_file, 'w', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(zip(urls, results))

# Example usage
input_csv_file = r'C:\Users\...\Input.csv'
output_csv_file = r'C:\Users\...\Output.csv'
check_phrases_in_csv(input_csv_file, output_csv_file)
