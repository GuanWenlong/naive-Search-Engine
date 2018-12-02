from elasticsearch_dsl import Text, Date, Keyword, Integer, Document, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer

connections.create_connection(hosts=["localhost"])

my_analyzer = analyzer('ik_smart')


class JobboleBlogIndex(Document):
    """伯乐在线文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_smart")

    class Index:
        name = 'jobble_new'