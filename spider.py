# _*_ coding: utf-8 _*_

"""
test.py by xianhu
"""

import spider
import logging
import datetime
import requests
from bs4 import BeautifulSoup
import re

black_patterns = (spider.CONFIG_URL_ILLEGAL_PATTERN, r"binding", r"download", )
white_patterns = ()

def url_parse(baseurl,html_doc,keys,priority):
    url_list=[]
    soup = BeautifulSoup(html_doc, 'lxml')
    post_nodes = soup.select('#archive .floated-thumb .post-thumb a')
    next_node = soup.select('.next.page-numbers')
    if(len(post_nodes)!=0 and len(next_node)!=0):
        for node in post_nodes:
            url_list.append((spider.get_url_legal(node['href'],baseurl),keys,priority+1))
        url_list.append((spider.get_url_legal(next_node[0]['href'], baseurl),keys,priority+1))
    return url_list
def decodeHtml(url,html_doc):
    content={}
    soup = BeautifulSoup(html_doc, 'lxml')
    content['url']=url
    try:
        content['title']=soup.select('.entry-header h1')[0].text
    except:
        content['title']=None
    try:
        content['tags']=soup.select('p.entry-meta-hide-on-mobile a')[0].text
    except:
        content['tags']=None
    try:
        content['content']=soup.select('div.entry')[0].text
    except:
        content['content']=None

    return content

class MyFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):
        response = requests.get(url, params=None, headers={}, data=None, proxies=proxies, timeout=(3.05, 10))
        result = (response.status_code, response.url, response.text)
        return 1, result, True


class MyParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        status_code, url_now, html_text = content
        url_list= url_parse(url_now,html_text,keys,priority)

        title = re.search(r"<title>(?P<title>.+?)</title>", html_text, flags=re.IGNORECASE)
        save_list = [(url, title.group("title").strip(), datetime.datetime.now()), ] if title else []

        content_dict=decodeHtml(url,html_text)
        if content_dict==None:
            content_dict={}
        return 1, url_list, save_list,content_dict


def test_spider():
    """
    test spider
    """
    # initial fetcher / parser / saver
    fetcher = MyFetcher(max_repeat=3, sleep_time=1)
    parser = MyParser(max_deep=3)
    saver = spider.Saver(save_pipe=open("./spider/out_thread.txt", "w"))
    # define url_filter
    url_filter = spider.UrlFilter(black_patterns=black_patterns, white_patterns=white_patterns, capacity=None)

    # initial web_spider
    web_spider = spider.WebSpider(fetcher, parser, saver, proxieser=None, url_filter=url_filter, max_count=10, max_count_in_proxies=100)

    # add start url
    web_spider.set_start_url("http://blog.jobbole.com/all-posts/", priority=0, keys={}, deep=0)

    # start web_spider
    web_spider.start_working(fetcher_num=10)

    # wait for finished
    web_spider.wait_for_finished()
    return


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")
    test_spider()
    exit()
