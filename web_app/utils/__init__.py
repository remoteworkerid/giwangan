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

def readfile(filename):
    returndata = ''
    try:
        fd = open(filename, 'r')
        text = fd.read()
        fd.close()
        returndata = text
    except:
        print('COULD NOT LOAD:', filename)
    return returndata