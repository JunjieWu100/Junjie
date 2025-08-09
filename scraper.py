from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup ChromeDriver service
service = Service(ChromeDriverManager().install())

# Initialize the Chrome WebDriver with the Service object
driver = webdriver.Chrome(service=service)

# Open BBC News website
driver.get("https://www.bbc.com/news")

# Wait for the headlines to be fully loaded on the page (up to 10 seconds)
wait = WebDriverWait(driver, 10)
headlines = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h2[data-testid="card-headline"]')))

# Print the headlines
for headline in headlines:
    print(headline.text)

# Close the browser
driver.quit()
