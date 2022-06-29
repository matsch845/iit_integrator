from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import pandas as pd

from matcher_strict import start_matching

es = Elasticsearch(['localhost:9200'])

es.info()


def get_data_from_elastic(table_name):
    query = {
        "query": {
            "match_all": {}
        }
    }

    rel = scan(client=es,
               query=query,
               scroll='1m',
               index=table_name,
               raise_on_error=True,
               preserve_order=False,
               clear_scroll=True)

    result = list(rel)
    temp = []

    for hit in result:
        temp.append(hit['_source'])

    df = pd.DataFrame(temp)
    return df


def get_statistics():
    df_integrated = get_data_from_elastic("integrated-dataset")

    filter = df_integrated["confidence_level"] < 3

    print("Integrations with confidence_level < 3: " + str(len(df_integrated[filter])))
    print("Total of integrations: " + str(len(df_integrated)))
    print("Different companies in articles: " + str(len(df_integrated['rb_company'].unique())))


if __name__ == '__main__':
    df_articles = get_data_from_elastic('article')
    df_corporate_events = get_data_from_elastic('corporate-events-full')

    print(df_articles)

    print('####################################################')
    print('####################################################')

    print(df_corporate_events)

    start_matching(df_articles, df_corporate_events)

    get_statistics()
