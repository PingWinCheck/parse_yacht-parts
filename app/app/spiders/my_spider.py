from typing import Any

import scrapy
from scrapy.http import Response


class SpiderMan(scrapy.Spider):
    name = 'spiderman'
    start_urls = ['https://yacht-parts.ru/catalog/']

    def parse(self, response: Response, **kwargs: Any) -> Any:
        categories = response.css('li.sect')
        for category_ in categories:  # type: Response
            category = category_.css('a::text').get()
            if category:
                category = category.strip()
            href = category_.css('a::attr(href)').get()
            yield response.follow(href, self.parse_products, meta={'category': category})

    def parse_products(self, response: Response, **kwargs: Any) -> Any:
        products = response.css('div.list_item_wrapp.item_wrap')
        for product in products:  # type: Response
            title = product.css('div.item-title a span::text').get()
            if title:
                title = title.strip()
            href = product.css('div.item-title a::attr(href)').get()
            yield response.follow(href, self.parse_card, meta={'category': response.meta.get('category'),
                                                               'title': title,
                                                               'href': href})
        next_page = response.css('li.flex-nav-next:not(.disabled) a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_products, meta={'category': response.meta.get('category')})

    def parse_card(self, response: Response, **kwargs: Any) -> Any:
        article = response.css('div.article.iblock span.value::text').get()
        if article:
            article = article.strip()
        price = response.css('div.price::text').get()
        if price:
            price = price.strip()
        description = response.css('div.preview_text::text').get()
        if description:
            description = description.strip()
        img = response.css('img::attr(src)').get()
        if img:
            img = img.strip()
        yield {'category': response.meta.get('category'),
               'article': article,
               'title': response.meta.get('title'),
               'price': price,
               'description': description,
               'img': img,
               'href': response.meta.get('href'),
               }


class BrandSpider(scrapy.Spider):
    name = 'brand'
    start_urls = ['https://yacht-parts.ru/info/brands/']

    def parse(self, response: Response, **kwargs: Any) -> Any:
        brands = response.css("ul.brands_list li a::attr(href)").getall()
        for brand in brands:  # type: str
            yield {'brand': brand.split('/')[-2].replace('_', ' ')}
        next_page = response.css('li.flex-nav-next:not(.disabled) a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
