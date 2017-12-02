def process(page):
    content = 'empty page content'
    if page is not None:
        content = page.content
    return content