import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import json

TWITTER_USERNAME = 'DattUpp83785'
TWITTER_PASSWORD = 'hello@123'

options = ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)
url = "https://twitter.com/i/flow/login"
driver.get(url)

try:

    username = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username.send_keys(TWITTER_USERNAME)
    username.send_keys(Keys.ENTER)

    password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys(TWITTER_PASSWORD)
    password.send_keys(Keys.ENTER)

    time.sleep(10)
    
    driver.get('https://twitter.com/home')
    time.sleep(10) 
    

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')


    trends_section = soup.find('div', {'aria-label': 'Timeline: Trending now'})
    trend_names = []

    if trends_section:
        trend_items = trends_section.find_all('div', {'data-testid': 'trend'})
        for item in trend_items[:5]:  # Get top 5 trends
            trend_name_element = item.find('span', class_='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3')
            if trend_name_element:
                trend_name = trend_name_element.get_text(separator=" ", strip=True)
                trend_names.append(trend_name)


    with open('result.json', 'w') as f:
        json.dump({"trends": trend_names}, f)

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
