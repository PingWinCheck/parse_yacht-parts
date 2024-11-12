# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas


class AppPipeline:
    def process_item(self, item, spider):
        return item


class ExcelSaver:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        df = pandas.DataFrame(self.items)
        df = df[['category', 'article', 'brand', 'title', 'price', 'description', 'img', 'link']]
        df = df.rename(columns={
            'category': 'Категория',
            'brand': "Бренд",
            'article': "Артикул",
            'title': "Наименование товара",
            'price': "Цена",
            'description': "Описание",
            'img': "Ссылки на изображения",
            'link': "Ссылка на товар",
        })
        df.to_excel('result.xlsx', index=False)
