import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re  # For extracting product ID

# ✅ Your Amazon affiliate tag
AFFILIATE_TAG = "dd1430e-21"

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False  # Ensure browser opens visibly

# Start ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Amazon Deals Page
url = "https://www.amazon.in/deals"
driver.get(url)

# ✅ Increase wait time to ensure page loads fully
time.sleep(10)

# ✅ Try multiple XPath variations
deal_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/dp/")]')

# Store extracted links
deals = []
for element in deal_elements:
    normal_link = element.get_attribute("href")
    if normal_link:
        # Extract product ID from the link (Amazon product ID is usually 10 characters long)
        match = re.search(r"/dp/([A-Z0-9]{10})", normal_link)
        if match:
            product_id = match.group(1)
            affiliate_link = f"https://www.amazon.in/dp/{product_id}?tag={AFFILIATE_TAG}"
            deals.append({"Normal Link": normal_link, "Affiliate Link": affiliate_link})

# Close the browser
driver.quit()

# Save to Excel if deals are found
if deals:
    df = pd.DataFrame(deals)
    file_path = "C:\\Users\\ELCOT\\Desktop\\amazon_deals_affiliated.xlsx"
    df.to_excel(file_path, index=False)
    print(f"✅ Affiliate links saved to {file_path}")
else:
    print("❌ No deals found. Try increasing wait time or checking XPath.")
