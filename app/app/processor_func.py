def strip(value: str) -> str:
    return value.strip() if value else ''


def url_join(url, loader_context) -> str:
    response = loader_context.get('response')
    return response.urljoin(url)


def clear_rub(value: str) -> str:
    result = value[:-5]
    result = result.replace(' ', '').replace('от', '')
    return result


def to_float(value: str) -> float:
    return float(value) if value else ''

