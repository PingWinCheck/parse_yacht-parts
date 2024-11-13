# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas
import os


class AppPipeline:
    def process_item(self, item, spider):
        return item


class ExcelSaver:
    def __init__(self):
        self.items = []
        self.excel_file_name = 'result.xlsx'

    def process_item(self, item, spider):
        self.items.append(ItemAdapter(item).asdict())
        # if len(self.items) >= 2:
        #     self.save()
        #     self.items.clear()
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.save()

    def save(self):
        df = pandas.DataFrame(self.items)

        if os.path.exists(self.excel_file_name):
            df_old = pandas.read_excel(self.excel_file_name)
            pandas.concat([df_old, df], ignore_index=True).to_excel(self.excel_file_name, index=False)
        else:
            # df = df[['category', 'article', 'brand', 'title', 'price', 'description', 'img', 'link']]
            df = df[['category', 'article', 'brand', 'title', 'price', 'description', 'img']]
            # df = df.rename(columns={
            #     'category': 'Категория',
            #     'brand': "Бренд",
            #     'article': "Артикул",
            #     'title': "Наименование товара",
            #     'price': "Цена",
            #     'description': "Описание",
            #     'img': "Ссылки на изображения",
            #     'link': "Ссылка на товар",
            # })
            df.to_excel(self.excel_file_name, index=False)
