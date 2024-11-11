def strip(value):
    return value.strip() if value else ''


def url_join(url, loader_context):
    response = loader_context.get('response')
    return response.urljoin(url)
