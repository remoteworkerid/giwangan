import urllib3
import bs4

url = 'https://trends.google.co.id/trends/'

http = urllib3.PoolManager()
result = http.request('GET', url)
if result.status == 200:
    res = bs4.BeautifulSoup(result.data, 'lxml')
    data = res.find('div', {'class': 'landing-page-hottrends-trends-list-container box'})
    print(data)