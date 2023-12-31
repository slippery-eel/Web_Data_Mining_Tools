### This script requires an input of a csv file with a list of webpages
### The script will crawl each page and output every hyperlink that is contained within each page, and output this list in a new csv file


import csv
import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    async with session.get(url, headers=headers, timeout=10) as response:
        content = await response.read()
        try:
            # Try decoding using UTF-8
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            # If decoding using UTF-8 fails, try decoding using ISO-8859-1 (Latin-1)
            text = content.decode('iso-8859-1')
        return text

async def extract_links_from_webpage(session, url):
    try:
        html = await fetch(session, url)
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    return links

async def extract_links_for_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            await asyncio.sleep(2)  # Add a delay of 2 seconds between requests
            tasks.append(extract_links_from_webpage(session, url))
        return await asyncio.gather(*tasks)

def extract_links_in_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)

        urls = [row[0].strip('\ufeff') for row in rows if row]

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(extract_links_for_urls(urls))

    with open(output_file, 'w', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.writer(csv_file)
        for url, links in zip(urls, results):
            for link in links:
                csv_writer.writerow([url, link])

# Example usage
input_csv_file = r'C:\Users\...\Input.csv'
output_csv_file = r'C:\Users\...\Output.csv'
extract_links_in_csv(input_csv_file, output_csv_file)
