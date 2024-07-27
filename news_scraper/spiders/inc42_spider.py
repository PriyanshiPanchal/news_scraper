import scrapy
from datetime import datetime


class EconomicsSpider(scrapy.Spider):
    name = 'inc42'
    start_urls = ['https://inc42.com/']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Extract links to individual articles
        # article_links = response.css('a[href*="/article/"]::attr(href)').getall()
        article_links = response.css('a[href*="/buzz/"]::attr(href)').getall()
        

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
        author_url = f"{author_url}" if author_url else None

        article_content = ' '.join(response.css('article p::text, div p::text, section p::text').getall()).strip()

        date_str = response.css('div.date span::text').get()
        published_date = None
        if date_str:
            # Parse the date string and format it to the desired format
            try:
                dt_object = datetime.strptime(date_str, "%d %b'%y")
                published_date = dt_object.strftime("%b %d, %Y, %I:%M:%S %p IST")
            except ValueError:
                published_date = "Unknown"

        yield {
            'Article URL': response.url,
            'Title': title,
            'Author Name': author_name,
            'Author URL': author_url,
            'Article Content': article_content,
            'Published Date': published_date
        }