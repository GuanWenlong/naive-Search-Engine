# _*_ coding: utf-8 _*_

"""
inst_save.py by xianhu
"""

import sys
import logging
from ..utilities import get_dict_buildin
from spider.ES_Init import JobboleBlogIndex,generate_suggests
from elasticsearch_dsl import connections

es_jobbole_blog = connections.create_connection(JobboleBlogIndex)
class Saver(object):
    """
    class of Saver, must include function working()
    """

    def __init__(self, save_pipe=sys.stdout):
        """
        constructor
        :param save_pipe: default sys.stdout, also can be a file handler
        """
        self._save_pipe = save_pipe
        return

    def working(self, url: str, keys: dict, item: (list, tuple),content:dict) -> int:
        """
        working function, must "try, except" and don't change the parameters and return
        :return save_state: can be -1(save failed), 1(save success)
        """
        logging.debug("%s start: keys=%s, url=%s", self.__class__.__name__, keys, url)

        try:
            save_state = self.item_save(url, keys, item)
        except Exception as excep:
            save_state = -1
            logging.error("%s error: %s, keys=%s, url=%s", self.__class__.__name__, excep, get_dict_buildin(keys), url)
        try:
            save_state_es=self.save2es(content)
        except:
            save_state_es=-1
            logging.debug("%s end: save_state=%s, url=%s", self.__class__.__name__, save_state_es, url)
        return save_state_es

    def item_save(self, url: str, keys: dict, item: (list, tuple)) -> int:
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        self._save_pipe.write("\t".join([str(col) for col in item]) + "\n")
        self._save_pipe.flush()
        return 1

    def save2es(self,content):
        blog=JobboleBlogIndex()

        blog.url=content['url']
        blog.content=content['content']
        blog.tags=content['tags']
        blog.title=content['title']
        blog.suggest = generate_suggests(es_jobbole_blog, JobboleBlogIndex,
                                         ((blog.title, 10), (blog.tags, 6), (blog.content, 4)))
        blog.save()
        return 1