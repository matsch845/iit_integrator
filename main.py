from datetime import datetime
from elasticsearch7 import Elasticsearch
from elasticsearch7.helpers import scan
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


df_articles = get_data_from_elastic('article')
df_corporate_events = get_data_from_elastic('corporate-events-full')

print(df_articles)

print('####################################################')
print('####################################################')

print(df_corporate_events)

start_matching(df_articles, df_corporate_events)
