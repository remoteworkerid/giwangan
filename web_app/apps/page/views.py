def process(page):
    if page is not None:
        return page.content, page.feature_image, page.title
    return 'Empty page'