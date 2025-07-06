from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def analyze_performance(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service("C:/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    start_time = time.time()
    driver.get(url)

    load_time = (time.time() - start_time) * 1000  # in ms

    timing = driver.execute_script("return window.performance.timing")
    first_paint = timing["responseStart"] - timing["navigationStart"]
    dom_loaded = timing["domContentLoadedEventEnd"] - timing["navigationStart"]
    total_load = timing["loadEventEnd"] - timing["navigationStart"]

    driver.quit()

    return {
        "time_to_first_byte_ms": round(first_paint, 2),
        "dom_content_loaded_ms": round(dom_loaded, 2),
        "total_page_load_time_ms": round(total_load, 2)
    }
