import scrapy
import re


class FoodSpider(scrapy.Spider):
    name = "food"
    # start_urls = [
    # "https://www.food.com/ideas/top-breakfast-recipes-6935#c-796349", 
    # "https://www.food.com/ideas/easy-lunch-recipes-7007", 
    # "https://www.food.com/ideas/top-appetizer-recipes-7009",
    # "https://www.food.com/ideas/all-time-best-dinner-recipes-6009",
    # "https://www.food.com/ideas/top-dessert-recipes-6930",
    # "https://www.food.com/ideas/summer-cocktails-drinks-6268",
    # "https://www.food.com/ideas/50-ultimate-side-dishes-6395",
    # "https://www.food.com/ideas/25-microwave-meals-for-busy-moms-6088",
    # "https://www.food.com/ideas/best-air-fryer-recipes-6847",
    # "https://www.food.com/ideas/best-instant-pot-recipes-6928",
    # "https://www.food.com/ideas/top-grilling-recipes-6974",
    # "https://www.food.com/ideas/slow-cooker-recipes-and-crock-pot-recipes-6017",
    # "https://www.food.com/ideas/top-dessert-recipes-6930",
    # "https://www.food.com/ideas/top-sheet-pan-recipes-6836",
    # "https://www.food.com/ideas/top-casserole-recipes-6016",
    # "https://www.food.com/ideas/winning-chili-recipes-6283",
    # "https://www.food.com/ideas/75-top-rated-recipes-of-all-time-6719",
    # "https://www.food.com/ideas/best-soup-recipes-6176",
    # "https://www.food.com/ideas/quick-easy-pasta-recipes-6078",
    # "https://www.food.com/ideas/best-homemade-bread-6912",
    # "https://www.food.com/ideas/cookie-recipes-7152",
    # "https://www.food.com/ideas/fun-salad-ideas-6301",
    # "https://www.food.com/ideas/best-tofu-recipes-7155",
    # "https://www.food.com/ideas/top-copycat-restaurant-recipes-6021",
    # "https://www.food.com/ideas/quick-easy-chicken-dinners-6013",
    # "https://www.food.com/ideas/best-salmon-recipes-6370",
    # "https://www.food.com/ideas/best-baked-pork-chops-6369",
    # "https://www.food.com/ideas/quick-easy-ground-beef-dinners-6011",
    # "https://www.food.com/ideas/top-shrimp-recipes-6566",
    # "https://www.food.com/ideas/keto-recipes-6652",
    # "https://www.food.com/ideas/top-healthy-recipes-6926",
    # "https://www.food.com/ideas/vegetarian-recipes-6323",
    # "https://www.food.com/ideas/best-vegan-recipes-6213",
    # "https://www.food.com/ideas/mediterranean-diet-recipes-6794",
    # "https://www.food.com/ideas/favorite-weight-watcher-recipes-6010",
    # "https://www.food.com/ideas/low-carb-recipes-6118",
    # "https://www.food.com/ideas/gluten-free-essentials-6320",
    # "https://www.food.com/ideas/top-appetizer-recipes-7009",
    # "https://www.food.com/ideas/top-game-day-recipes-6927",
    # "https://www.food.com/ideas/top-easter-recipes-6936",
    # "https://www.food.com/ideas/mexican-6528",
    # "https://www.food.com/ideas/top-mothers-day-recipes-6973",
    # "https://www.food.com/ideas/best-memorial-day-recipes-6972",
    # "https://www.food.com/ideas/juneteenth-food-ideas-7158",
    # "https://www.food.com/ideas/top-4th-of-july-recipes-6675",
    # "https://www.food.com/ideas/top-halloween-recipes-7012",
    # "https://www.food.com/ideas/regional-state-thanksgiving-food-6457",
    # "https://www.food.com/ideas/traditional-hanukkah-food-6159",
    # "https://www.food.com/ideas/top-holiday-recipes-6919",
    # "https://www.food.com/ideas/new-years-dinner-ideas-7145",
    # "https://www.food.com/ideas/mexican-food-at-home-6830",
    # "https://www.food.com/ideas/italian-food-recipes-at-home-6828",
    # "https://www.food.com/ideas/indian-food-recipes-at-home-6821",
    # "https://www.food.com/ideas/thai-food-recipes-at-home-6820",
    # "https://www.food.com/ideas/korean-food-recipes-at-home-7143",
    # "https://www.food.com/ideas/french-food-at-home-7129",
    # "https://www.food.com/ideas/best-latin-american-recipes-7133",
    # "https://www.food.com/ideas/chinese-food-at-home-6807",
    # "https://www.food.com/ideas/japanese-food-recipes-at-home-7140",
    # "https://www.food.com/ideas/spanish-food-recipes-at-home-7122",
    # "https://www.food.com/ideas/quick-and-easy-spring-dinners-6553",
    # "https://www.food.com/ideas/fresh-tomato-recipes-6273",
    # "https://www.food.com/ideas/quick-and-easy-fall-dinners-6554",
    # "https://www.food.com/ideas/winter-dinner-6543"
    # ]


    # def parse(self, response):
    #     recipe_links = response.css(".smart-cards .smart-card.container-sm.recipe .smart-info-wrap a::attr(href)").extract()

    #     for link in recipe_links:
    #         yield scrapy.Request(url=link, callback=self.parse_recipe)

    def start_requests(self):
        with open('links.txt', 'r') as f:
            urls = f.read().splitlines()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_recipe)

    def parse_recipe(self, response):
        title = response.css(".layout__item.title h1::text").get()
        image_url = response.css(".layout__item.media .media .primary-image:first-child img::attr(src)").get()

        ingredients_array = []
        ingredient_items = response.css(".layout__item.ingredients ul.ingredient-list li")

        for item in ingredient_items:
            quantity_html = item.css(".ingredient-quantity").extract_first()
            quantity = self.extract_quantity(quantity_html)
            ingredient_text = "".join(item.css(".ingredient-text *::text").getall()).strip()

            combined_ingredient = f"{quantity} {ingredient_text}".strip()
            combined_ingredient = re.sub(r'\s+', ' ', combined_ingredient)

            if combined_ingredient:
                ingredients_array.append(combined_ingredient)

        directions_array = response.css(".layout__item.directions ul.direction-list li.direction::text").getall()
        directions_array = [direction.strip() for direction in directions_array if direction.strip()]

        description = response.xpath("//*[@id='recipe']/div[5]/div/div[2]/div/div//text()").getall()
        description = ' '.join([desc.strip() for desc in description if desc.strip()])
        description = description.strip('\"')

        # Facts
        facts_array = []
        facts_items = response.css('.facts__item')
        for item in facts_items:
            label = item.css('.facts__label::text').get()

            # Extract text content without HTML tags
            value = item.css('.facts__value').xpath('string()').get().lower().strip()

            # Check if both label and value are present
            if label and value:
                label = label.lower().replace(' ', '_').strip()
                facts_array.append({label.strip(): value.strip()})

        # nutrition_info = {}

        # # Extract general information
        # nutrition_info['serving_size'] = response.css('.recipe-nutrition__main-info p:nth-child(2)::text').get().strip()
        # nutrition_info['servings_per_recipe'] = response.css('.recipe-nutrition__main-info p:nth-child(3)::text').get().strip()

        # # Extract detailed nutrition information
        # nutrition_sections = response.css('.recipe-nutrition__info .recipe-nutrition__section')
        # for section in nutrition_sections:
        #     nutrient_name = section.css('.recipe-nutrition__item span::text').get().strip()
        #     nutrient_value = section.css('.recipe-nutrition__item::text').getall()[1].strip()
        #     nutrient_percent = section.css('.recipe-nutrition__item span.svelte-epeb0m:last-child::text').get().strip()

        #     nutrition_info[nutrient_name] = {
        #         'value': nutrient_value,
        #         'percent': nutrient_percent
        #     }
        
        yield {
            "facts": facts_array,
            "description": description,
            "title": title,
            "image_url": image_url,
            "recipe_link": response.url,
            "ingredients": ingredients_array,
            "directions": directions_array,
        }

    def extract_quantity(self, quantity_html):
        quantity = scrapy.Selector(text=quantity_html).xpath("string()").get() if quantity_html else None
        quantity = re.sub(r'\s+', ' ', quantity) if quantity else ""
        return quantity