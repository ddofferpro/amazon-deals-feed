import time
import re
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# ✅ Your Amazon affiliate tag
AFFILIATE_TAG = "dd1430e-21"

# ✅ Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True  # Run in headless mode for GitHub Actions

# ✅ Start ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ Open Amazon Deals Page
url = "https://www.amazon.in/deals"
driver.get(url)
time.sleep(10)  # Ensure page loads

# ✅ Extract product links
deal_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/dp/")]')
deals = []

for element in deal_elements:
    normal_link = element.get_attribute("href")
    if normal_link:
        match = re.search(r"/dp/([A-Z0-9]{10})", normal_link)
        if match:
            product_id = match.group(1)
            affiliate_link = f"https://www.amazon.in/dp/{product_id}?tag={AFFILIATE_TAG}"
            deals.append({"Title": f"Amazon Deal - {product_id}", "Link": affiliate_link})

# ✅ Close the browser
driver.quit()

# ✅ Generate RSS Feed
if deals:
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Amazon Deals RSS Feed"
    ET.SubElement(channel, "link").text = "https://yourgithubusername.github.io/amazon-deals-feed/amazon_deals.xml"
    ET.SubElement(channel, "description").text = "Daily updated Amazon deals with affiliate links."

    for deal in deals:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = deal["Title"]
        ET.SubElement(item, "link").text = deal["Link"]
        ET.SubElement(item, "description").text = "Limited-time deal on Amazon."

    # ✅ Save as XML file
    tree = ET.ElementTree(rss)
    tree.write("amazon_deals.xml", encoding="utf-8", xml_declaration=True)
    print("✅ RSS Feed generated successfully: amazon_deals.xml")
else:
    print("❌ No deals found.")

