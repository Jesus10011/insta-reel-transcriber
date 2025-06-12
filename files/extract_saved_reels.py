from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def extract_reel_urls(scroll_count=5):
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=/home/jesoh/.config/selenium-profile")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1200,800")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.instagram.com/jesoh_1010/saved/programming/18045035735135004/")
    time.sleep(5)

    reels = []

    # Scroll to load more content
    for i in range(scroll_count):

        anchors = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
        print(f"Found {len(anchors)} links")

        for i, a in enumerate(anchors):
            try:
                post_href = a.get_attribute("href")
                if post_href and "/p/" in post_href:
                    reel_url = post_href.replace("/p/", "/reel/")
                    print(f"[{i+1}] {reel_url}")
                    reels.append(reel_url)
            except Exception as e:
                print(f"[{i+1}] Error: {e}")
                continue

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"Scrolled {i+1}")
        time.sleep(2)



    driver.quit()

    # Remove duplicates and save to file
    unique_reels = list(set(reels))
    with open("reel_urls.txt", "w") as f:
        for url in unique_reels:
            f.write(url + "\n")

    print(f"\nSaved {len(unique_reels)} reel URLs to reel_urls.txt")
    return unique_reels