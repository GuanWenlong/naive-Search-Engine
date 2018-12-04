
from bs4 import BeautifulSoup
import requests
response = requests.get('http://blog.jobbole.com/114427/', params=None, headers={}, data=None, timeout=(3.05, 10))

soup = BeautifulSoup(response.text, 'lxml')
for node in soup.select('.digg-item-updated-title a'):
    print(node['href'])
    # print(node)