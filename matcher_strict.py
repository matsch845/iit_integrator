import json
import re
from fuzzywuzzy import fuzz
from nltk import ngrams
import pandas as pd
from Levenshtein import distance as levenshtein_distance
from elasticsearch import Elasticsearch

es = Elasticsearch(['localhost:9200'])


def create_json(key, file_name):
    data = {key: []}
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)


def write_json(new_data, filename='out_data.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        # Join new_data with file_data inside company_news
        file_data["company_news"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def find_company(inp):
    start = inp.find(":")
    end = inp.find(",")
    company = inp[start + 2:end]

    if (len(company) == 0):
        company = inp[0:inp.find(",")]

    return company


def clean_it(inp):
    clean = re.sub('/[^a-zäöüßA-Zäöüß0-9 ]/g+', ' ', inp).lower().strip()
    clean = re.sub(r'[^\w\s]', ' ', clean)
    clean = re.sub(' +', ' ', clean)
    return clean


create_json("company_news", "out_data.json")


# carful this creates new emtpy json


def start_matching(df_news):
    # this is expensive matching:

    # for u in range(len(df_news)): for testing only 100:
    # CHANGE THIS FOR PR
    for u in range(len(df_news)):
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

        split = news_search_keyword.split('%')

        rb_id = split[1]
        company = split[0]
        company = clean_it(company)
        print(company)
        n_gram_amount = len(company.split())
        print(n_gram_amount)

        check_grams = []
        n = n_gram_amount
        n_grams = ngrams(title.split(), n)

        for grams in n_grams:
            check_grams.append(grams)
        check = []

        for item in check_grams:
            check.append(' '.join(item))

        print(check)

        for item in check:
            distance_set = fuzz.token_set_ratio(item, company)
            distance_sort = fuzz.token_sort_ratio(item, company)
            leven_dist = levenshtein_distance(item, company)
            print(distance_set, distance_sort, leven_dist)

            print("'" + item + "' matched with: '" + company + "'")

            confidence_level = (1 / leven_dist * (distance_set + distance_sort)) / (200)

            es.index(
                index='integrated-dataset',
                body={
                    "unique_rb_news": str(str(rb_id) + str(news_id)),
                    "rb_company": company,
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
