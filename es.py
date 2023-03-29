import sys
import json

from tqdm import tqdm
from elasticsearch import Elasticsearch

SPECIAL_CHAR = ['(', ')', '{', '}', '[', ']', '^', '~', '/', ':', '?', '!']
SPECIAL_CHAR2 = ["'", '"']


class ElasticSearch:
    def __init__(self):
        self.es = Elasticsearch(hosts="localhost")

    def all_index(self):
        print(self.es.cat.indices(format=json, pretty=True))

    def delete_index(self, index_name=None):
        self.es.indices.delete(index=index_name)

    def create_index(self, index_name=None):
        self.es.indices.create(
            index=index_name,
            body={
                "settings": {
                    "number_of_replicas": 0,
                    "analysis": {
                        "analyzer": {
                            "my_analyer": {
                                "tokenizer": "nori_mixed",
                                "filter": ["my_synonym",
                                           "lowercase",
                                           "nori_readingform",
                                           "nori_number",
                                           "cjk_bigram",
                                           "decimal_digit",
                                           "stemmer",
                                           "trim"]
                            }
                        },
                        "filter": {
                            "my_synonym": {
                                "type": "synonym",
                                "lenient": True,
                                "synonyms_path": "user_dic/my_syn_dic.txt"
                            }
                        },
                        "tokenizer": {
                            "nori_mixed": {
                                "type": "nori_tokenizer",
                                "decompound_mode": "mixed",
                                "user_dictionary": "user_dic/userdict.txt"
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "context": {"type": "text", "analyzer": "my_analyer"},
                    }
                }
            }
        )

    def insert_data(self, index_name=None, file_name=None):
        with open(f"context_data/{file_name}", "r", encoding="utf-8") as fjson:
            data = json.load(fjson)["data"]

        for row in tqdm(data, desc=f'{index_name}'):
            row_id = row['id']
            doc = {'title': row['row']['title'], 'context': row['row']['context']}
            res = self.es.index(index=index_name, id=row_id, document=doc)['_shards']
            assert res['failed'] == 0, row_id + '\t' + doc["context"]


    def search(self, index_name=None, question=None):
        question = self.preprocess_query(question)
        res = self.es.search(
            index=index_name,
            body={
                "size": 5,
                "query": {
                    "query_string": {
                        "default_field": "context",
                        "query": question
                    }
                }
            }
        )

        retrival_result_list = []
        for hit in res['hits']['hits']:
            es_id = hit['_id']
            title = hit['_source']['title']
            context = hit['_source']['context']
            em_score = hit['_score']
            retrival_result_list.append([es_id, context, title, em_score])

        return retrival_result_list

    @staticmethod
    def special_char(text):
        for char in SPECIAL_CHAR:
            text = text.replace(char, '\{}'.format(char))
        for char in SPECIAL_CHAR2:
            text = text.replace(char, '\\{}'.format(char))
        return text

    @staticmethod
    def preprocess_query(query):
        if '언제인가' in query:
            query = query.replace('언제인가', '')
        if '어디인가' in query:
            query = query.replace('어디인가', '')
        if '무엇인가' in query:
            query = query.replace('무엇인가', '')
        if '누구인가' in query:
            query = query.replace('누구인가', '')

        return query


if __name__ == '__main__':
    args = sys.argv
    es = ElasticSearch()
    print(args)

    # 데이터 index 조회
    if args[1] == 'index':
        es.all_index()

    # 데이터 index 삭제
    if args[1] == 'delete':
        es.delete_index(index_name=args[2]) # args[2] == index_name

    # 데이터 index 생성
    if args[1] == 'create':
        es.create_index(index_name=args[2])  # args[2] == index_name

    # 데이터 삽입 (insert)
    if args[1] == 'insert':
        es.insert_data(index_name=args[2], file_name=args[3])  # args[2] == index_name
