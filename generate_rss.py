import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# ✅ Your Amazon affiliate tag
AFFILIATE_TAG = "dd1430e-21"

# ✅ Setup Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True  # Run in background
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ Visit Amazon Deals page
url = "https://www.amazon.in/deals"
driver.get(url)
time.sleep(10)

# ✅ Find deal links
deal_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/dp/")]')

# ✅ Extract deals
seen = set()
rss_items = []

for element in deal_elements:
    link = element.get_attribute("href")
    if link:
        match = re.search(r"/dp/([A-Z0-9]{10})", link)
        if match:
            product_id = match.group(1)
            if product_id in seen:
                continue
            seen.add(product_id)

            affiliate_link = f"https://www.amazon.in/dp/{product_id}?tag={AFFILIATE_TAG}"
            title = f"Amazon Deal - {product_id}"
            guid = f"https://www.amazon.in/dp/{product_id}"
            pub_date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')

            rss_items.append(f"""
    <item>
        <title>{title}</title>
        <link>{affiliate_link}</link>
        <description>Top deal on Amazon India</description>
        <guid>{guid}</guid>
        <pubDate>{pub_date}</pubDate>
    </item>""")

driver.quit()

# ✅ Build RSS Feed XML
rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Amazon Deals Feed</title>
    <link>https://www.amazon.in/deals</link>
    <description>Today's top Amazon deals with affiliate links</description>
    <lastBuildDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>
    {''.join(rss_items)}
</channel>
</rss>
"""

# ✅ Save to XML file
output_path = "amazon_deals.xml"
with open(output_path, "w", encoding="utf-8") as file:
    file.write(rss_feed)

print(f"✅ RSS feed generated and saved to {output_path}")
