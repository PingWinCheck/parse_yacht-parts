import logging
from typing import Any, Iterable

import scrapy

from scrapy.http import Response

from ..items import Product
from ..processor_func import strip, url_join
from scrapy.loader import ItemLoader
# from scrapy.loader.processors import TakeFirst, MapCompose
from itemloaders.processors import TakeFirst, MapCompose, Join


class SpiderMan(scrapy.Spider):
    name = 'spiderman2'
    start_urls = ['https://yacht-parts.ru/catalog/']

    def parse(self, response: Response, **kwargs: Any) -> Any:
        categories = response.css('li.sect')
        for category_ in categories[:1]:  # type: Response
            category = category_.css('a::text').get()
            if category:
                category = category.strip()
            href = category_.css('a::attr(href)').get()
            yield response.follow(href, self.parse_products, meta={'category': category})

    def parse_products(self, response: Response, **kwargs: Any) -> Any:
        products = response.css('div.list_item_wrapp.item_wrap')
        for product in products[:1]:  # type: Response
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
        loader = ItemLoader(item=Product(), response=response)
        loader.default_input_processor = MapCompose(strip)
        loader.default_output_processor = TakeFirst()
        loader.add_value('category', response.meta.get('category'))
        loader.add_css('article', 'div.article.iblock span.value::text')
        loader.add_css('brand', "a.brand_picture img::attr(title)")
        loader.add_value('title', response.meta.get('title'))
        loader.add_css('price', 'div.price::text')
        loader.add_css('description', 'div.preview_text::text')
        loader.add_css('img', 'div.offers_img.wof img::attr(src)')
        loader.add_css('img', "div.slides li a::attr(href)", MapCompose(url_join), Join(', '))
        loader.add_value('link', response.urljoin(response.meta.get('href')))
        yield loader.load_item()


class BrandSpider(scrapy.Spider):
    name = 'brand2'
    start_urls = ['https://yacht-parts.ru/info/brands/']

    def parse(self, response: Response, **kwargs: Any) -> Any:
        brands = response.css("ul.brands_list li a::attr(href)").getall()
        for brand in brands:  # type: str
            yield {'brand': brand.split('/')[-2].replace('_', ' ')}
        tag = getattr(self, 'tagg', None)
        if tag is not None:
            next_page = response.css('li.flex-nav-next:not(.disabled) a::attr(href)').get()
            if next_page:
                yield response.follow(next_page, self.parse)
