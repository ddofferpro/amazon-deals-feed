import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from datetime import datetime

def generate_rss(deals, output_file="rss.xml"):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "Amazon Deals Feed"
    ET.SubElement(channel, "link").text = "https://www.amazon.in/gp/goldbox"
    ET.SubElement(channel, "description").text = "Today's top Amazon deals with affiliate links"

    for deal in deals[:30]:  # take first 30 deals
        item = ET.SubElement(channel, "item")
        title = escape(deal.get("title", "No Title"))
        link = deal.get("link", "")
        # Ensure '&' in link is escaped
        link = escape(link, {"&": "&amp;"})
        description = escape(deal.get("price", "No Price"))

        ET.SubElement(item, "title").text = title
        ET.SubElement(item, "link").text = link
        ET.SubElement(item, "description").text = description
        ET.SubElement(item, "pubDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

    tree = ET.ElementTree(rss)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
