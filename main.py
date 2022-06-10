from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import scan
import pandas as pd

es = Elasticsearch(['localhost:9200'])

es.info()

def get_data_from_elastic(table_name):
    
    query = {
        "query" : {
            "match_all" : {}
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
df_corporate_events = get_data_from_elastic('corporate-events')

print(df_articles)

print('####################################################')
print('####################################################')

print(df_corporate_events)

df_articles.to_csv('article.csv', sep=',')
df_articles.to_csv('corporate-events.csv', sep=',')