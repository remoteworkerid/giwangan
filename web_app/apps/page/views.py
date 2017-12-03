def process(page):
    content = 'empty page content'
    feature_image = None
    if page is not None:
        content = page.content
        feature_image = page.feature_image

    return content, feature_image