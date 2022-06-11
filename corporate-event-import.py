import json
import pandas as pd
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import scan

es = Elasticsearch(['localhost:9200'])

chunks = pd.read_json("corporate-events-dump", lines=True, chunksize=10000)

counter = 1

for chunk in chunks:
    print("##################################################" + str(counter))

    for data in chunk._source:
        print(data["id"])
        es.index(
            index='corporate-events-full',
            body={
            'id': data["id"],
            'rb_id': data["rb_id"],
            'state': data["state"],
            'event_type': data["event_type"],
            'event_date' : data["event_date"],
            'status': data["status"],
            'information': data["information"]
        })

    counter += 1