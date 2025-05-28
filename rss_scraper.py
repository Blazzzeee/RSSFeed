import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import logging
import uuid
from datetime import datetime, timezone
from collections import defaultdict

# Configure logging
logging.basicConfig(
    format='%(levelname)s | %(message)s',
    level=logging.INFO
)

# List of RSS feeds to scrape
rss_feeds = [
    {"country": "United Kingdom", "source": "BBC", "url": "http://feeds.bbci.co.uk/news/rss.xml"},
    {"country": "United States", "source": "CNN", "url": "http://rss.cnn.com/rss/edition.rss"},
    {"country": "Qatar", "source": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml"},
    {"country": "Japan", "source": "NHK", "url": "https://www3.nhk.or.jp/rss/news/cat0.xml"},
    {"country": "India", "source": "The Hindu", "url": "https://www.thehindu.com/news/national/feeder/default.rss"},
    {"country": "Singapore", "source": "CNA", "url": "https://www.channelnewsasia.com/rssfeeds/8395986"},
    {"country": "Malaysia", "source": "The Star", "url": "https://www.thestar.com.my/rss/editors-pick"},
    {"country": "Indonesia", "source": "Kompas", "url": "https://rss.kompas.com/"},
    {"country": "South Korea", "source": "Korea Times", "url": "https://www.koreatimes.co.kr/www/rss/rss.xml"},
    {"country": "China", "source": "China Daily", "url": "https://www.chinadaily.com.cn/rss/china_rss.xml"},
    {"country": "Germany", "source": "DW", "url": "https://rss.dw.com/rdf/rss-en-all"},
    {"country": "France", "source": "France 24", "url": "https://www.france24.com/en/rss"},
    {"country": "Canada", "source": "CBC", "url": "https://www.cbc.ca/cmlink/rss-topstories"},
    {"country": "Australia", "source": "ABC", "url": "https://www.abc.net.au/news/feed/51120/rss.xml"},
    {"country": "Brazil", "source": "Folha de S.Paulo", "url": "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml"},
    {"country": "Russia", "source": "RT", "url": "https://www.rt.com/rss/news/"},
    {"country": "South Africa", "source": "News24", "url": "https://www.news24.com/rss?sectionId=1"},
    {"country": "Mexico", "source": "El Universal", "url": "http://www.eluniversal.com.mx/rss.xml"},
    {"country": "Turkey", "source": "Hurriyet Daily News", "url": "https://www.hurriyetdailynews.com/rss"},
    {"country": "Italy", "source": "ANSA", "url": "https://www.ansa.it/sito/ansait_rss.xml"},
    {"country": "Spain", "source": "El País", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"},
]

# List to store news items
news_items = []

# Maximum number of retries for fetching a feed
MAX_RETRIES = 3

async def fetch_rss(session, feed):
    """
    Fetch and parse RSS feed, appending news items to the global list.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"[{feed['source']}] Fetching attempt {attempt}")
            headers = {'User-Agent': 'Mozilla/5.0'}
            async with session.get(feed["url"], headers=headers, timeout=20) as response:
                response.raise_for_status()
                content = await response.read()
                soup = BeautifulSoup(content, "xml")
                items = soup.find_all("item")
                if not items:
                    logging.warning(f"[{feed['source']}] No items found.")
                for item in items:
                    news_items.append({
                        "id": str(uuid.uuid4()),
                        "title": item.title.text if item.title else None,
                        "link": item.link.text if item.link else None,
                        "pubDate": item.pubDate.text if item.pubDate else None,
                        "description": item.description.text if item.description else None,
                        "source": feed["source"],
                        "country": feed["country"],
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                logging.info(f"[{feed['source']}] Successfully fetched {len(items)} items.")
                return
        except Exception as e:
            logging.warning(f"[{feed['source']}] Error on attempt {attempt}: {e}")
            await asyncio.sleep(2)
    logging.error(f"[{feed['source']}] Failed after {MAX_RETRIES} retries.")

async def main():
    """
    Main function to orchestrate fetching of all RSS feeds.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_rss(session, feed) for feed in rss_feeds]
        await asyncio.gather(*tasks)

    logging.info(f"Fetched a total of {len(news_items)} articles from {len(rss_feeds)} feeds.")

    # Save all news items to a single JSON file
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)
    logging.info("All data saved to news_data.json")

if __name__ == "__main__":
    asyncio.run(main())
