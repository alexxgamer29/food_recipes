import scrapy
from scrapy import signals

class TastyKitchenSpider(scrapy.Spider):
    name = 'tastykitchen'
    start_urls = ['http://tastykitchen.com/recipes/']
    not_found_urls = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.handle_response_received, signal=signals.response_received)
        crawler.signals.connect(spider.handle_spider_closed, signal=signals.spider_closed)
        return spider

    def handle_response_received(self, response, request, spider):
        if response.status == 404:
            self.not_found_urls.append(response.url)

    def handle_spider_closed(self, spider, reason):
        with open('not_found_urls.txt', 'w') as f:
            for url in self.not_found_urls:
                f.write(f'{url}\n')

    def parse(self, response):
        # Generate URLs for all pages
        for page_number in range(1, 8448):
            page_url = f'https://tastykitchen.com/recipes/page/{page_number}/'
            yield scrapy.Request(url=page_url, callback=self.parse_page, meta={'page_number': page_number})

    def parse_page(self, response):
        try:
            recipe_links = response.css('.c6-1234 a.h3::attr(href)').extract()

            # Extract page number from the meta
            page_number = response.meta.get('page_number', None)
            for link in recipe_links:
                yield scrapy.Request(url=link, callback=self.parse_recipe, meta={'page_number': page_number})

        except Exception as e:
            self.log(f'Error on page {response.url}: {e}')

    def parse_recipe(self, response):
        try:
            # Extract page number from the meta
            page_number = response.meta.get('page_number', None)
            # Title
            title = response.css("h1[itemprop='name']::text").get()
            # Image URL
            image_url = response.css("img.the_recipe_image::attr(src)").get()
            # Categories
            categories = response.css("a[rel='category tag']::text").getall()
            categories = [category.lower() for category in categories]
            # Description
            description = response.css("span[itemprop='summary'] p::text").get()
            # Ingredients
            ingredients = response.css("ul.ingredients li")
            ingredients_data = []
            for ingredient in ingredients:
                amount = None
                name = ingredient.css("span[itemprop='name']::text").get()
                amount_element = ingredient.css("span[itemprop='amount']::text")
                if amount_element:
                    amount = amount_element.get()
                ingredients_data.append({"amount": amount, "name": name})

            yield {
                "page_number": page_number,
                "description": description,
                "ingredients": ingredients_data,
                "title": title,
                "image_url": image_url,
                "categories": categories,
                "url": response.url,
            }
        except Exception as e:
            self.log(f'Error on page {response.url}: {e}')

    # def parse_page(self, response):
    #     try:
    #         recipe_titles = response.css('.c6-1234 a.h3::text').extract()
    #         self.log(f'Recipe Titles on page {response.url}: {recipe_titles}')

    #         # Extract page number from the meta
    #         page_number = response.meta.get('page_number', None)

    #         yield {
    #             "page_number": page_number,
    #             "title": recipe_titles,
    #             "url": response.url,
    #         }
    #     except Exception as e:
    #         self.log(f'Error on page {response.url}: {e}')