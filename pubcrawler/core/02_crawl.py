# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/core/02_crawl.ipynb.

# %% auto 0
__all__ = ['chrome_options', 'service', 'driver', 'visited_urls', 'file_links', 'url', 'base_domain', 'file_type',
           'scroll_to_bottom', 'pubcrawl']

# %% ../../nbs/core/02_crawl.ipynb 4
import pubcrawler as proj
from .. import const, log, utils, tools
import adu_proj.utils as adutils

# %% ../../nbs/core/02_crawl.ipynb 5
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from time import sleep
import pandas as pd
import json

# %% ../../nbs/core/02_crawl.ipynb 7
chrome_options = Options()
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")  # Necessary for some versions of Chrome

# %% ../../nbs/core/02_crawl.ipynb 8
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# %% ../../nbs/core/02_crawl.ipynb 9
visited_urls = set()
file_links = {}

# %% ../../nbs/core/02_crawl.ipynb 10
url = const.url
base_domain = urlparse(url).netloc
file_type = const.file_type

# %% ../../nbs/core/02_crawl.ipynb 11
def scroll_to_bottom(driver, # Selenium driver 
                     timeout=2
                    ):
    "Scroll to the bottom of the webpage to ensure all content is loaded."
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for the page to load
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return document.body.scrollHeight") > last_height
            )
            # Update the last height for next scroll
            last_height = driver.execute_script("return document.body.scrollHeight")
        except TimeoutException:
            # If no new content is loaded within the timeout, break the loop
            break

# %% ../../nbs/core/02_crawl.ipynb 12
def pubcrawl(url: str, # url to get links for 
          visited_urls: set, # urls that have already been visited by crawl
          file_type: str, # type of file to get ie 'pdf'
          file_links: dict, # dictionary of links to files found by crawl
          driver, # Selenium webdriver 
          base_domain: str # base domain for url
            ):
    "Get the urls for all files of a specified type from subpages of a url"
    if url in visited_urls:
        return
    print(url)
    visited_urls.add(url)
    for attempt in range(2):
        try:
            driver.get(url)
            break  # If successful, exit the loop
        except Exception as e:
            if attempt < 1:  # Only retry once
                print(f"Retrying {url} due to error: {e}")
                continue
            else:
                print(f"Failed to access {url} after retrying: {e}")
                return  # Skip to the next URL if both attempts fail
    if url == base_domain:
        sleep(5)
    scroll_to_bottom(driver)  # Scroll to bottom to load everything
    # sleep(1)
    links = driver.find_elements(By.TAG_NAME, "a")
    # hrefs = [link.get_attribute('href') for link in links if link.is_displayed() and link.get_attribute('href') not in visited_urls]
    hrefs = [link.get_attribute('href') for link in links if link.get_attribute('href') not in visited_urls]
    for href in hrefs:
        if href and href.endswith(f".{file_type}"):
            # print(f"this one: {href}")
            file_links.setdefault(href, {'parent_links': []}).setdefault('parent_links', []).append(url)
        elif href and urlparse(href).netloc == base_domain and '#' not in href.split('/')[-1] and '.' not in href.split('/')[-1]:
            pubcrawl(href, visited_urls, file_type, file_links, driver, base_domain)

# %% ../../nbs/core/02_crawl.ipynb 15
print("𝔏𝔢𝔱 𝔱𝔥𝔢 𝔠𝔯𝔞𝔴𝔩 𝔠𝔬𝔪𝔪𝔢𝔫𝔠𝔢... 𝔓𝔯𝔬𝔰𝔱! 🍺🍺🍺")
print("\nSites visited:")
pubcrawl(url, visited_urls, file_type, file_links, driver, urlparse(url).netloc)
print("\nℭ𝔯𝔞𝔴𝔩 𝔠𝔬𝔪𝔭𝔩𝔢𝔱𝔢 💀💀💀")
print(f"Visited {len(visited_urls)} webpages")

# %% ../../nbs/core/02_crawl.ipynb 17
# pd.DataFrame([{'file_link': key, 'parent_links': file_links[key]['parent_links']} for key in file_links]).to_csv(f'{const.pre_output_path}/files.csv', index=False)
with open(f'{const.pre_output_path}/data.json', 'w') as f:
    json.dump(file_links, f)
