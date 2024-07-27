import scrapy

class LivemintSpider(scrapy.Spider):
    name = 'livemint'
    start_urls = ['https://www.livemint.com']
    
    def start_requests(self):
        # Set headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Extract links to individual articles
        # print("Response Text:")
        article_links = response.css('a[href*="/news/"]::attr(href)').getall()
        print("Links:", article_links)
        print("Length of Article Links:", len(article_links))
        for link in article_links:
            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get() or response.xpath('//h1/text()').get()
        
        author_name = response.css('a[href*="/authors/"]::text').get()
        # author_name = response.css('span[class*="author"] a::text').get()
        if not author_name:
            author_name = response.css('span.premiumarticleInfo.premiumauthor a::text').get(),
        author_name = author_name.strip() if author_name else 'Unknown'

        author_url = response.css('a[href*="/authors/"]::attr(href)').get()
        author_url = f"https://www.livemint.com{author_url}" if author_url else None
        
        article_content = ' '.join(response.css('article p::text, div p::text, section p::text').getall()).strip()
        
        published_date = response.css('span[id^="tBox_"]::attr(data-updatedlongtime)').get()
        if not published_date:
            published_date = response.css('span[class*="metaDate"]::text').re_first(r'\d{2} \w{3} \d{4}')
        
        yield {
            'Article URL': response.url,
            'Title': title,
            'Author Name': author_name,
            'Author URL': author_url,
            'Article Content': article_content,
            'Published Date': published_date
        }

    # def parse_article(self, response):
        
    #     yield {
    #         'Article URL': response.url,
    #         'Title': response.css('h1::text').get(),
    #         # 'Author Name': response.css('a.author-name::text').get(),
    #         'Author Name': response.css('span.premiumarticleInfo.premiumauthor a::text').get().strip(),
    #         'Author URL': f"https://www.livemint.com{response.css('span.premiumarticleInfo.premiumauthor a::attr(href)').get()}",
    #         'Article Content': ' '.join(response.css('div.mainArea p::text').getall()).strip(),
    #         'Published Date': response.css('span[id^="tBox_"]::attr(data-updatedlongtime)').get()
        # }
