# News Scraper

This project contains a set of web scraping spiders built with Scrapy for extracting news articles from various websites. It includes spiders for:

1. **Live Mint**
2. **Economic Times**
3. **Inc42**

## Project Structure

- `spiders/`: Contains individual spider files for each website.
- `inc42_spider.py`: Spider for scraping news from Inc42.
- `economics_spider.py`: Spider for scraping news from Economic Times.
- `livemint_spider.py`: Spider for scraping news from Live Mint.
- `news_scraper/`: The main Scrapy project directory.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/news_scraper.git
   cd news_scraper

## Run the Inc42 Spider

scrapy runspider spiders/inc42_spider.py -o inc42_articles.json

## Run the Economic Times Spider

scrapy runspider spiders/economics_spider.py -o economics_articles.json

## Run the Live Mint Spider

scrapy runspider spiders/livemint_spider.py -o livemint_articles.json
