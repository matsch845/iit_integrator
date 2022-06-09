from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import scan
import pandas as pd


# ELASTIC_PASSWORD = "elastic"

# # Found in the 'Manage Deployment' page
# CLOUD_ID = "http://es01-test:9200"

# # Create the client instance
# client = Elasticsearch(
#     cloud_id=CLOUD_ID,
#     basic_auth=("elastic", ELASTIC_PASSWORD)
# )

# # Successful response!
# client.info()

es = Elasticsearch(['localhost:9200'])

es.info()

def get_data_from_elastic(table_name):
    # query: The elasticsearch query.
    query = {
        "query" : {
            "match_all" : {}
        }
    }
    # Scan function to get all the data. 
    rel = scan(client=es,             
               query=query,                                     
               scroll='1m',
               index=table_name,
               raise_on_error=True,
               preserve_order=False,
               clear_scroll=True)

    # Keep response in a list.
    result = list(rel)
    temp = []
    # We need only '_source', which has all the fields required.
    # This elimantes the elasticsearch metdata like _id, _type, _index.
    for hit in result:
        temp.append(hit['_source'])
    # Create a dataframe.
    df = pd.DataFrame(temp)
    return df

df_articles = get_data_from_elastic('article')
df_corporate_events = get_data_from_elastic('corporate-events')

print(df_articles)
print('####################################################')
print('####################################################')
print(df_corporate_events)