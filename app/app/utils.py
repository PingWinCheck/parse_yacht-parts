from functools import lru_cache


@lru_cache
def load_brands() -> list[str]:
    with open('brands.txt') as f:
        file = f.read()
        return file.split(', ')


def checkout_brand_file_in_title(title: str):
    brand_list = load_brands()
    for brand in brand_list:
        if brand.lower() in title.lower():
            return brand
    return ''
