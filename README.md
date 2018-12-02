# naive-Search-Engine （一个幼稚的搜索引擎）
A naive Search Engine based on ElasticSearch, the spider part is based on the work [Spider](https://github.com/anuragranj/spynet.). The web part is based on the Flask framework.

##Usage
1. Install the required package through pipenv.

pipenv install

2. Install the [Elastic Search](https://www.elastic.co/) (v6.5.0) as well as the [IK Analysis plugin](https://github.com/medcl/elasticsearch-analysis-ik) and run

./elasticsearch-6.5.0/bin/elasticsearch

3. Run the spider part through pipenv.

pipenv run python spider.py


4. Run the web part with

pipenv run python flask/app.py 

