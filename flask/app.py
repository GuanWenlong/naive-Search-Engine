import os

from flask import render_template,request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask import Flask
from elasticsearch import Elasticsearch
import redis
import pickle

client = Elasticsearch(hosts=["localhost"])
# 使用redis实现top-n排行榜
redis_cli = redis.StrictRedis()

app = Flask(__name__)
app.debug = True
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/search')
def search():
    key_words = request.args.get("q", "")
    # 通用部分
    # 实现搜索关键词keyword加1操作
    # redis_cli.zincrby("search_keywords_set", key_words,1.0)
    # 获取topn个搜索词
    topn_search_clean = []
    topn_search = redis_cli.zrevrangebyscore(
        "search_keywords_set", "+inf", "-inf", start=0, num=5)
    for topn_key in topn_search:
        topn_key = str(topn_key, encoding="utf-8")
        topn_search_clean.append(topn_key)
    topn_search = topn_search_clean
    # 获取伯乐在线的文章数量

    jobbole_count = redis_cli.get("jobbole_blog_count")
    if jobbole_count:
        jobbole_count = pickle.loads(jobbole_count)
    else:
        jobbole_count = 0

    # 当前要获取第几页的数据
    page = request.args.get("p", "1")
    try:
        page = int(page)
    except BaseException:
        page = 1
    response = client.search(
        index="jobble_new",
        request_timeout=60,
        body={
            "query": {
                "multi_match": {
                    "query": key_words,
                    "fields": ["tags", "title", "content"]
                }
            },
            "from": (page - 1) * 10,
            "size": 10,
            "highlight": {
                "pre_tags": ['<span class="keyWord">'],
                "post_tags": ['</span>'],
                "fields": {
                    "title": {},
                    "content": {},
                }
            }
        }
    )

    # 伯乐在线具体的信息
    hit_list = []
    error_nums = 0
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        try:
            if "title" in hit["highlight"]:
                hit_dict["title"] = "".join(hit["highlight"]["title"])
            else:
                hit_dict["title"] = hit["_source"]["title"]
            if "content" in hit["highlight"]:
                hit_dict["content"] = "".join(
                    hit["highlight"]["content"])
            else:
                hit_dict["content"] = hit["_source"]["content"][:200]
            hit_dict["create_date"] = "none"
            hit_dict["url"] = hit["_source"]["url"]
            hit_dict["score"] = hit["_score"]
            hit_dict["source_site"] = "伯乐在线"
            hit_list.append(hit_dict)
        except:
            error_nums = error_nums + 1
    total_nums = int(response["hits"]["total"])

    # 计算出总页数
    if (page % 10) > 0:
        page_nums = int(total_nums / 10) + 1
    else:
        page_nums = int(total_nums / 10)

    return render_template('return_search.html',
                           page=page,
                           all_hits=hit_list,
                           key_words=key_words,
                           total_nums=total_nums,
                           page_nums=page_nums,
                           topn_search=topn_search,
                           jobbole_count=jobbole_count,
                           )

if __name__ == '__main__':
    app.run(debug=True)
