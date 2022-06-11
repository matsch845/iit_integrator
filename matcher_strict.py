import json
import re
from fuzzywuzzy import fuzz
from nltk import ngrams
import pandas as pd
from Levenshtein import distance as levenshtein_distance
from elasticsearch import Elasticsearch, RequestsHttpConnection
es = Elasticsearch(['localhost:9200'])


def create_json(key, file_name):
    data = {key: []}
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)


def write_json(new_data, filename='out_data.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        # Join new_data with file_data inside company_news
        file_data["company_news"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)


def find_company(inp):
    start = inp.find(":")
    end = inp.find(",")
    company = inp[start+2:end]
    return company


def clean_it(inp):
    clean = re.sub('/[^a-zäöüßA-Zäöüß0-9 ]/g+', ' ', inp).lower().strip()
    clean = re.sub(r'[^\w\s]', ' ', clean)
    clean = re.sub(' +', ' ', clean)
    return clean


create_json("company_news", "out_data.json")
# carful this creates new emtpy json


def start_matching(df_news, df_rb):
    # this is expensive matching:
    for i in range(len(df_rb)):
        rb_id = df_rb["id"][i]
        info = df_rb["information"][i]
        status = df_rb["status"][i]
        event_date = df_rb["event_date"][i]
        event_type = df_rb["event_type"][i]

        company = find_company(info)
        company = clean_it(company)
        print(company)
        n_gram_amount = len(company.split())
        print(n_gram_amount)

        # for u in range(len(df_news)): for testing only 100:
        # CHANGE THIS FOR PR
        for u in range(1000):
            news_link = df_news["link"][u]
            news_id = df_news["id"][u]
            news_publication_date = df_news["publication_date"][u]
            news_description = df_news["description"][u]
            news_source = df_news["source"][u]
            news_search_keyword = df_news["search_keyword"][u]
            news_search_url = df_news["search_url"][u]
            title = df_news["title"][u]
            title = clean_it(title)
            print(title)

            check_grams = []
            n = n_gram_amount
            n_grams = ngrams(title.split(), n)

            for grams in n_grams:
                check_grams.append(grams)
            check = []

            for item in check_grams:
                check.append(' '.join(item))

            print(check)

            threshold_set = 75
            threshold_sort = 75
            threshold_leven = 10

            for item in check:
                distance_set = fuzz.token_set_ratio(item, company)
                distance_sort = fuzz.token_sort_ratio(item, company)
                leven_dist = levenshtein_distance(item, company)
                print(distance_set, distance_sort, leven_dist)
                if distance_set >= threshold_set and distance_sort >= threshold_sort and leven_dist < threshold_leven:
                    print("'" + item + "' matched with: '" + company + "'")

                    confidence_level = (1/leven_dist * (distance_set + distance_sort)) / (200)
                    
                    es.index(
                        index='integrated-dataset',
                        body={
                        "unique_rb_news": str(str(rb_id) + str(news_id)),
                        "rb_company": company,
                        "event_type": event_type,
                        "event_date": event_date,
                        "status": status,
                        "rb_id": rb_id,
                        "news_link": news_link,
                        "news_id": news_id,
                        "news_publication_date": news_publication_date,
                        "news_description": news_description,
                        "news_source": news_source,
                        "news_search_keyword": news_search_keyword,
                        "news_search_url": news_search_url,
                        "title": title,
                        "confidence_level": confidence_level
                    })

                    break
                else:
                    print("nothing matched in: " + item + "____" + company)
                    # do we want companies without news in output or no? right now they are not in there, but we could add
                    # here, idk lets discuss


