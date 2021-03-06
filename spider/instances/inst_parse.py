# _*_ coding: utf-8 _*_

"""
inst_parse.py by xianhu
"""

import re
import logging
import datetime
from ..utilities import CONFIG_PARSE_MESSAGE, get_dict_buildin


class Parser(object):
    """
    class of Parser, must include function working()
    """

    def __init__(self, max_deep=0):
        """
        constructor
        :param max_deep: default 0, if -1, spider will not stop until all urls are fetched
        """
        self._max_deep = max_deep
        return

    def working(self, priority: int, url: str, keys: dict, deep: int, content: object) -> (int, list, list):
        """
        working function, must "try, except" and don't change the parameters and return
        :return parse_state: can be -1(parse failed), 1(parse success)
        :return url_list: [(url1, keys1, priority1), (url2, keys2, priority2), ...]
        :return save_list: [item1(a list or tuple), item2(a list or tuple), ...]
        """
        logging.debug("%s start: %s", self.__class__.__name__, CONFIG_PARSE_MESSAGE % (priority, keys, deep, url))

        content_dict={}
        parse_state, url_list, save_list,content_dict = self.htm_parse(priority, url, keys, deep, content)

        # except Exception as excep:
        #     print("****")
        #     parse_state, url_list, save_list = -1, [], []
        #     logging.error("%s error: %s, %s,here", self.__class__.__name__, excep, CONFIG_PARSE_MESSAGE % (priority, get_dict_buildin(keys), deep, url))
        logging.debug("%s end: parse_state=%s, len(url_list)=%s, len(save_list)=%s, url=%s", self.__class__.__name__, parse_state, len(url_list), len(save_list), url)

        # try:
        #     parse_state, url_list, save_list,content_dict = self.htm_parse(priority, url, keys, deep, content)
        # except Exception as excep:
        #     print("****")
        #     parse_state, url_list, save_list = -1, [], []
        #     logging.error("%s error: %s, %s,here", self.__class__.__name__, excep, CONFIG_PARSE_MESSAGE % (priority, get_dict_buildin(keys), deep, url))
        # logging.debug("%s end: parse_state=%s, len(url_list)=%s, len(save_list)=%s, url=%s", self.__class__.__name__, parse_state, len(url_list), len(save_list), url)
        return parse_state, url_list, save_list,content_dict

    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object) -> (int, list, list,list):
        """
        parse the content of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        status_code, url_now, html_text = content

        print("***")
        url_list = []
        if (self._max_deep < 0) or (deep < self._max_deep):
            url_list = [(_url, keys, priority+1) for _url in re.findall(r"<a.+?href=\"(?P<url>.{5,}?)\".*?>", html_text, flags=re.IGNORECASE)]

        title = re.search(r"<title>(?P<title>.+?)</title>", html_text, flags=re.IGNORECASE)
        save_list = [(url, title.group("title").strip(), datetime.datetime.now()), ] if title else []
        content_list={}
        # content_list['title']=
        return 1, url_list, save_list,content_list
