import scrapy
import re

class NotFoundURLSpider(scrapy.Spider):
    name = 'notfoundurl'
    
    def start_requests(self):
        with open('not_found_urls.txt', 'r') as f:
            urls = f.read().splitlines()
        for url in urls:
            page_number = re.search(r'/page/(\d+)/', url)
            if page_number:
                page_number = page_number.group(1)
            self.log(f'*** Page {page_number}')
            yield scrapy.Request(url=url, callback=self.parse_page, meta={'page_number': page_number})

    def parse_page(self, response):
        try:
            recipe_titles = response.css('.c6-1234 a.h3::text').extract()
            self.log(f'Recipe Titles on page {response.url}: {recipe_titles}')

            # Extract page number from the meta
            page_number = response.meta.get('page_number', None)

            yield {
                "page_number": page_number,
                "title": recipe_titles,
                "url": response.url,
            }
        except Exception as e:
            self.log(f'Error on page {response.url}: {e}')