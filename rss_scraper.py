import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import logging

logging.basicConfig(
    format='%(levelname)s | %(message)s',
    level=logging.INFO
)

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
    {"country": "Mexico", "source": "El Universal", "url": "https://archivo.eluniversal.com.mx/rss/portada.xml"},
    {"country": "South Africa", "source": "News24", "url": "https://www.news24.com/rss"},
    {"country": "Turkey", "source": "Hurriyet Daily News", "url": "https://www.hurriyetdailynews.com/rss"},
    {"country": "Italy", "source": "ANSA", "url": "https://www.ansa.it/sito/ansait_rss.xml"},
    {"country": "Spain", "source": "El País", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"},
]

news_items = []

async def fetch_rss(session, feed):
    try:
        logging.info(f"Sending request to: {feed['url']} ({feed['source']} - {feed['country']})")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        async with session.get(feed["url"], headers=headers, timeout=20) as response:
            logging.info(f"Received response {response.status} from {feed['source']}")
            response.raise_for_status()
            content = await response.read()
            soup = BeautifulSoup(content, "xml")
            items = soup.find_all("item")
            if not items:
                logging.warning(f"No items found in feed: {feed['url']}")
            for item in items:
                news_items.append({
                    "title": item.title.text if item.title else None,
                    "link": item.link.text if item.link else None,
                    "pubDate": item.pubDate.text if item.pubDate else None,
                    "description": item.description.text if item.description else None,
                    "source": feed["source"],
                    "country": feed["country"]
                })
    except Exception as e:
        logging.error(f"Failed to fetch {feed['url']}: {e}")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_rss(session, feed) for feed in rss_feeds]
        await asyncio.gather(*tasks)

    logging.info(f"Fetched {len(news_items)} articles from {len(rss_feeds)} feeds.")
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)
    logging.info("Data saved to news_data.json")

if __name__ == "__main__":
    asyncio.run(main())
