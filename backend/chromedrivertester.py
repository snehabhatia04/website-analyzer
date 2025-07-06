from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set path to chromedriver.exe
service = Service(executable_path=r"C:\chromedriver.exe")

# Optional: for headless (if you don't want a visible Chrome window)
options = Options()
# options.add_argument("--headless")  # Uncomment this for headless mode

# Initialize driver
driver = webdriver.Chrome(service=service, options=options)

# Go to Google and print title
driver.get("https://www.google.com")
print(driver.title)

# Close browser
driver.quit()
