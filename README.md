# RSSFeed

A Python script to scrape and store news articles from RSS feeds.

## Data Summary
| Country         | News Agencies | Total Articles | Total Historical Data |
| --------------- | ------------- | -------------- | --------------------- |
| Qatar           | Al Jazeera    | 25             | Since 2025            |
| Singapore       | CNA           | 20             | Since 2025            |
| India           | The Hindu     | 100            | Since 2025            |
| Australia       | ABC           | 25             | Since 2025            |
| France          | France 24     | 24             | Since N/A             |
| China           | China Daily   | 100            | Since N/A             |
| United Kingdom  | BBC           | 34             | Since N/A             |
| Italy           | ANSA          | 28             | Since 2025            |
| Canada          | CBC           | 20             | Since N/A             |
| Germany         | DW            | 151            | Since N/A             |
| United States   | CNN           | 50             | Since N/A             |
| Japan           | NHK           | 7              | Since 2025            |
| Russia          | RT            | 100            | Since 2025            |
| South Korea     | Korea Times   | 96             | Since N/A             |
| Spain           | El País       | 136            | Since N/A             |


## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Blazzzeee/RSSFeed.git
cd RSSFeed
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, you can manually install the required packages. For example:

```bash
pip install requests beautifulsoup4
```

*Note: Ensure you have the necessary permissions or use `sudo` where applicable.*

## ▶️ Running the Script

Execute the script to start scraping:

```bash
python rss_scraper.py
```

Ensure that the script is correctly configured to fetch the desired RSS feeds.

## 📄 Data Storage

The script stores the scraped news articles in a file named `news_data.json`. Ensure you have write permissions in the directory where the script is executed.
