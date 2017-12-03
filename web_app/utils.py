import re


def get_safe_url(text):
    """
    From title of post, into valid safe url
    :param text:
    :return:
    """
    url = text.replace(' ', '-').lower()
    regex = re.compile('[^a-zA-Z\-]')
    return regex.sub('', url).lower()