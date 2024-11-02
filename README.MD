# Парсинг сайта yacht-parts.ru

Получение полного каталога товаров и выгрузка их в json файл в формате:

```json
[
  {
    "category": "example", 
    "article": "example", 
    "title": "example",
    "price": "example", 
    "description": "example",
    "img": "example",
    "href": "example"
  }
]
```
При необходимости выгрузки в excel файл с дополнительным полем "брэнды" выполнить пункты [4,5](#команды-для-ввода-в-терминале-корневой-директории-проекта)
### Для запуска необходимо следующее:
Установлен python3.12, poetry 

необходимые ссылки

https://python-poetry.org/docs/#installing-with-the-official-installer

https://www.python.org/downloads/

### Команды для ввода в терминале корневой директории проекта
1) poetry install
2) cd app
3) scrapy crawl spiderman -O output.json
4) scrapy crawl brand -O brands.json
5) python brand_connector_dump_excel.py
