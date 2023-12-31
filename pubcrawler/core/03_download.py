# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/core/03_download.ipynb.

# %% auto 0
__all__ = ['file_folder', 'file_dir', 'options', 'download_file']

# %% ../../nbs/core/03_download.ipynb 4
import pubcrawler as proj
from .. import const, log, utils, tools
import adu_proj.utils as adutils

# %% ../../nbs/core/03_download.ipynb 5
import json
import os
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from tqdm import tqdm
from urllib.parse import unquote

# %% ../../nbs/core/03_download.ipynb 6
file_folder = const.file_type
file_dir = os.path.join(const.pre_output_path, file_folder)
os.makedirs(file_dir, exist_ok=True)

# %% ../../nbs/core/03_download.ipynb 7
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option("prefs", {
    "download.default_directory": file_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "plugins.always_open_pdf_externally": True
})

# %% ../../nbs/core/03_download.ipynb 8
with open(f'{const.pre_output_path}/data.json', 'r') as f:
    file_links = json.load(f)

# %% ../../nbs/core/03_download.ipynb 9
def download_file(file_url: str, # file url
                 download_dir: str, # directory to download file to 
                 ):
    "Download file to directory"
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)    
        driver.get(file_url)
        # Wait for the download to complete with checks
        filename = file_url.split('/')[-1]
        max_wait = 90
        wait_interval = 1
        file_path = os.path.join(download_dir, filename)
        temp_file_path = file_path + ".crdownload"    
        start_time = time.time()
        time.sleep(wait_interval)
        while not os.path.exists(file_path):
            if os.path.exists(temp_file_path):
                time.sleep(wait_interval)
            else:
                break
            if time.time() - start_time > max_wait:
                    print("Download timed out.")
                    break
        # Verify download and close the browser
        driver.close()
        driver.quit()
        # print(file_path)
        if os.path.isfile(unquote(file_path)):
            return unquote(file_path)
        else:
            print(f"Download failed for {file_url}")
            return None
    except WebDriverException as e:
        print(f"An error occurred while trying to download the file: {e}")
        driver.close()
        driver.quit()
        return None  

# %% ../../nbs/core/03_download.ipynb 10
for key in tqdm(file_links):
    file_links[key]['file_path'] = download_file(key, file_dir)

# %% ../../nbs/core/03_download.ipynb 11
with open(f'{const.pre_output_path}/data_files.json', 'w') as f:
    json.dump(file_links, f)
