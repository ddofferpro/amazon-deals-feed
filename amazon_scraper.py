import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

AFFILIATE_TAG = "dd1430e-21"

# Setup Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Headless for GitHub Actions
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Go to Amazon
url = "https://www.amazon.in/deals"
driver.get(url)
time.sleep(10)

deal_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/dp/")]')

deals = []
for element in deal_elements:
    href = element.get_attribute("href")
    match = re.search(r"/dp/([A-Z0-9]{10})", href)
    if match:
        product_id = match.group(1)
        affiliate_link = f"https://www.amazon.in/dp/{product_id}?tag={AFFILIATE_TAG}"
        deals.append({"Affiliate Link": affiliate_link})

driver.quit()

# Save as RSS XML
if deals:
    with open("amazon_deals.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
        f.write('<rss version="2.0"><channel>\n')
        f.write('<title>Amazon Deals Feed</title>\n')
        f.write('<link>https://www.amazon.in/deals</link>\n')
        f.write('<description>Latest Amazon India Deals</description>\n')
        for deal in deals:
            f.write('<item>\n')
            f.write(f"<title>Amazon Deal</title>\n")
            f.write(f"<link>{deal['Affiliate Link']}</link>\n")
            f.write(f"<guid>{deal['Affiliate Link']}</guid>\n")
            f.write(f"<pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>\n")
            f.write('</item>\n')
        f.write('</channel></rss>\n')
    print("✅ amazon_deals.xml RSS file generated.")
else:
    print("❌ No deals found.")


