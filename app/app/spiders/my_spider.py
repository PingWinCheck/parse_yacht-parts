import logging
from typing import Any, Iterable

import scrapy

from scrapy.http import Response

from ..items import Product
from ..processor_func import strip, url_join, clear_rub, to_float
from scrapy.loader import ItemLoader
# from scrapy.loader.processors import TakeFirst, MapCompose
from itemloaders.processors import TakeFirst, MapCompose, Join
from ..utils import checkout_brand_file_in_title

class SpiderMan(scrapy.Spider):
    name = 'spiderman'
    start_urls = ['https://yacht-parts.ru/catalog/']

    def parse(self, response: Response, **kwargs: Any) -> Any:
        categories = response.css('li.sect')
        for category_ in categories:  # type: Response
            category: str | None = category_.css('a::text').get()
            if category:
                category = category.strip()
            href = category_.css('a::attr(href)').get()
            yield response.follow(href, self.parse_products, meta={'category': category})

    def parse_products(self, response: Response, **kwargs: Any) -> Any:
        products = response.css('div.list_item_wrapp.item_wrap')
        for product in products:  # type: Response
            title: str | None = product.css('div.item-title a span::text').get()
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
        # loader.default_input_processor = MapCompose(strip)
        loader.default_output_processor = TakeFirst()
        loader.add_value('category', response.meta.get('category'))
        loader.add_css('article', 'div.article.iblock span.value::text')
        loader.add_css('brand', "a.brand_picture img::attr(title)")
        loader.add_value('title', response.meta.get('title'))
        loader.add_css('price', 'div.price::text', MapCompose(strip, clear_rub, to_float))
        loader.add_css('description', 'div.preview_text::text')
        loader.add_css('img', 'div.offers_img.wof img::attr(src)')
        loader.add_css('img', "div.slides li a::attr(href)", MapCompose(url_join), Join(', '))
        loader.add_value('link', response.urljoin(response.meta.get('href')))
        if not loader.get_output_value('brand'):
            loader.add_value('brand', checkout_brand_file_in_title(loader.get_output_value('title')))
        yield loader.load_item()

