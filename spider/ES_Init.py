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

def generate_suggests(es_con, index, info_tuple):
    es = es_con
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            words = es.indices.analyze(index="jobble_new", body={"analyzer": "ik_max_word", "text": "{0}".format(text)})
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests



if __name__ == "__main__":
    JobboleBlogIndex.init()
