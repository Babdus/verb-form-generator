import os
import sys
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


PAUSE_TIME = 0.1


def setup_driver(download_tmp_dir):
    options = Options()
    # options.add_argument('--headless')  # if you want to see the browser, comment this line
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('prefs', {
        "download.default_directory": download_tmp_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "profile.default_content_setting_values.automatic_downloads": 1
    })
    # print('Options set')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('http://gnc.gov.ge/gnc/corpus-list')
    # print('Got the website')

    wait = WebDriverWait(driver, 20)
    time.sleep(PAUSE_TIME)

    # Find the correct corpus row and click it
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    # print('Got table_rows')
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 4 and "ქართული ენის რეფერენციალური კორპუსი" in cells[3].text:
            # print('Found referential corpus')
            time.sleep(PAUSE_TIME)
            cells[3].click()
            break
    else:
        raise Exception("Corpus not found.")

    # Click the search button
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='შერჩეულ კორპუს(ებ)ში ძიება']")))
    time.sleep(PAUSE_TIME)
    search_button.click()

    # print('clicked button ძიება')

    return driver

def wait_for_download_to_finish(download_dir):
    seconds = 0
    time.sleep(PAUSE_TIME)
    while True:
        files = os.listdir(download_dir)
        if any(fname.endswith(".crdownload") for fname in files):
            time.sleep(1)
            seconds += 1
            if seconds > 300:
                raise Exception("Download took too long!")
        else:
            break

def download_word(driver, download_tmp_dir, download_final_dir, word: str, first_word=True):
    wait = WebDriverWait(driver, 20)
    time.sleep(PAUSE_TIME)
    # print('Got driver')

    wait.until(EC.presence_of_element_located((By.ID, "queryString")))
    query_input = driver.find_element(By.ID, "queryString")
    query_input.clear()
    query_input.send_keys(word)
    time.sleep(PAUSE_TIME)

    # print('Put in query string')

    if first_word:
        new_query_button = driver.find_element(By.ID, "newQuery")
    else:
        new_query_button = driver.find_element(By.NAME, "new-query")
    new_query_button.click()

    # print('Click on find')
    time.sleep(PAUSE_TIME)

    # Record files before download
    before_files = set(os.listdir(download_tmp_dir))

    if first_word:
        attrs_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'ატრიბუტები …')]")))
        # print('Found ატრიბუტები')
        attrs_button.click()
        # print('Clicked ატრიბუტები')
        time.sleep(PAUSE_TIME)
        # Click "ყველა" button
        all_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='ყველა']")))
        # print('Found ყველა')
        all_button.click()
        # print('Clicked ყველა')
        time.sleep(PAUSE_TIME)
        use_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='გამოაყენე']")))
        # print('Found გამოაყენე')
        use_button.click()
        # print('Clicked გამოაყენე')
        time.sleep(PAUSE_TIME)

    # Click download link
    download_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'downloadConcordance')]")))
    # print('Found download')
    download_link.click()
    # print('Click on download')

    time.sleep(PAUSE_TIME)

    # Wait for download to finish
    wait_for_download_to_finish(download_tmp_dir)
    # print('Download finished')
    time.sleep(PAUSE_TIME)

    # Find the new file
    after_files = set(os.listdir(download_tmp_dir))
    new_files = after_files - before_files
    # print(new_files)

    if len(new_files) != 1:
        raise Exception(f"Expected 1 new file, but found {len(new_files)} new files.")

    new_file = new_files.pop()
    old_path = os.path.join(download_tmp_dir, new_file)
    new_path = os.path.join(download_final_dir, f"{word}.txt")
    shutil.move(old_path, new_path)
    while True:
        if len(set(os.listdir(download_tmp_dir)) - before_files) == 0:
            break
        time.sleep(PAUSE_TIME)
        # print('Still not moved')
    # print(f"Downloaded and saved as: {new_path}")


def calculate_color(percent):
    if percent <= 25:
        color = 31
    elif percent <= 50:
        color = 33
    elif percent <= 75:
        color = 32
    else:
        color = 36
    return color


def download_words(driver, tmp_dir, final_dir, words):
    l = len(words)
    for i, word in enumerate(words):
        p = (i * 100) // l
        n = (i * 44) // l
        c = calculate_color(p)
        print(f'\033[32mDownloading... \033[34;1m{word:24}\t\033[0;35m{p}%\033[0m')
        print(f'\033[{c}m{"█" * n}\033[0m', end='')
        download_word(driver, tmp_dir, final_dir, word, first_word=i==0)
        # time.sleep(0.3)
        print('\r', end='')
        print('\x1b[1A', end='')
        if i == l - 1:
            p = ((i + 1) * 100) // l
            n = ((i + 1) * 44) // l
            c = calculate_color(p)
            print(f'\033[32mDownloading... \033[34;1m{word:24}\t\033[0;35m{p}%\033[0m')
            print(f'\033[{c}m{"█" * n}\033[0m')


def main(args):
    base_download_dir = "downloads"
    tmp_dir = '/home/tato/Downloads'
    final_dir = os.path.join(base_download_dir, "final")

    # Make sure folders exist
    # os.makedirs(tmp_dir, exist_ok=True)
    os.makedirs(final_dir, exist_ok=True)

    # Setup driver
    driver = setup_driver(tmp_dir)

    # Download a list of words
    words = []

    download_words(driver, tmp_dir, final_dir, words)

    driver.quit()


if __name__ == "__main__":
    main(sys.argv[1:])