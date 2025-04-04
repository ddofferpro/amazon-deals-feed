import time
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

# ✅ Your Amazon affiliate tag
AFFILIATE_TAG = "dd1430e-21"

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True  # Headless mode for automation

# Start ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Amazon Deals Page
url = "https://www.amazon.in/deals"
driver.get(url)
time.sleep(10)  # Wait for page to load

# Find deal elements
deal_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/dp/")]')

# Store affiliate links
deals = []
for element in deal_elements:
    normal_link = element.get_attribute("href")
    if normal_link:
        match = re.search(r"/dp/([A-Z0-9]{10})", normal_link)
        if match:
            product_id = match.group(1)
            affiliate_link = f"https://www.amazon.in/dp/{product_id}?tag={AFFILIATE_TAG}"
            deals.append({"Normal Link": normal_link, "Affiliate Link": affiliate_link})

driver.quit()

# ✅ Create RSS XML feed
rss = Element('rss')
rss.set('version', '2.0')

channel = SubElement(rss, 'channel')

title = SubElement(channel, 'title')
title.text = "Amazon Deals Feed"

link = SubElement(channel, 'link')
link.text = "https://www.amazon.in/deals"

description = SubElement(channel, 'description')
description.text = "Today's top Amazon deals with affiliate links"

# Add each deal as an RSS item
for deal in deals:
    item = SubElement(channel, 'item')

    item_title = SubElement(item, 'title')
    item_title.text = "Amazon Deal"

    item_link = SubElement(item, 'link')
    item_link.text = deal["Affiliate Link"]

    item_description = SubElement(item, 'description')
    item_description.text = "Promoted via affiliate"

    item_guid = SubElement(item, 'guid')
    item_guid.text = deal["Affiliate Link"]

# ✅ Save the XML to file
xml_str = parseString(tostring(rss)).toprettyxml(indent="  ")
output_path = os.path.join(os.getcwd(), "amazon_deals.xml")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(xml_str)

print(f"✅ RSS feed generated and saved to {output_path}")
