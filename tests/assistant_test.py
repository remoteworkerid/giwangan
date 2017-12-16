import json
import unittest


from assistant.core import AssistantCore


class TestAssistant(unittest.TestCase):

    def test_fetch_url(self):
        url = 'https://www.rd.com/advice/travel/top-10-most-extreme-travel-adventures-in-the-world/'
        core = AssistantCore()
        result, status, type = core.get(url)
        result = json.loads(result)

        self.assertTrue('Popular sports include skiing, ice hockey and ice fishing.' in
                        result['result']['text'])
        self.assertEqual(result['result']['images'][10]['src'],
                         'https://www.rd.com/wp-content/uploads/2017/11/03_Chile_These-Are-the-Top-10-Most-Extreme-'
                         'Travel-Adventures-in-the-World_561125371_Circumnavigation-760x506.jpg')

