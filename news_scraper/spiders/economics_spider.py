import scrapy
from datetime import datetime


class EconomicsSpider(scrapy.Spider):
    name = 'economics'
    start_urls = ['https://economictimes.indiatimes.com']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Extract links to individual articles
        # article_links = response.css('a[href*="/article/"]::attr(href)').getall()
        article_links = response.css('a[href*="/news/"]::attr(href)').getall()
        print("Links:", article_links)
        print("Length of Article Links:", len(article_links))
        for link in article_links:
            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get() or response.xpath('//h1/text()').get()

        author_name = response.css('a[href*="/author"]::text').get()
        if not author_name:
            author_name = response.css('span.author-name::text').get()
        author_name = author_name.strip() if author_name else 'Unknown'

        author_url = response.css('a[href*="/author"]::attr(href)').get()
        author_url = f"https://economictimes.indiatimes.com{author_url}" if author_url else None

        article_content = ' '.join(response.css('article p::text, div p::text, section p::text').getall()).strip()

        timestamp = response.css('time[data-dt]::attr(data-dt)').get()
        published_date = None
        if timestamp:
            # Convert timestamp from milliseconds to seconds
            timestamp = int(timestamp) / 1000
            # Create a datetime object
            dt_object = datetime.fromtimestamp(timestamp)
            # Format the datetime object to the desired format
            published_date = dt_object.strftime("%b %d, %Y, %I:%M:%S %p IST")

        yield {
            'Article URL': response.url,
            'Title': title,
            'Author Name': author_name,
            'Author URL': author_url,
            'Article Content': article_content,
            'Published Date': published_date
        }