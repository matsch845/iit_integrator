# IIT-Integrator

## Import corporate-events-dump
1. Get the corporate-events-dump (RB dataset) as discussed in slack
2. Run `python corporate-event-import` to import the dataset into elastic search

## General Architecture and Functionality

After importing the corporate-events-dump, main.py assings the confidence score to our google news data containig the company from the RB dat (integrator "matcher_strict")

The integrator works this way:
1. It takes the information of RB crawl and finds the company in the string via regex. (depending on where the company is written)
2. Use the cleaned company string as keyword to crawl google news
3. Check the returned news for actually containing the company and how confident we are in the news actually containing the company.
4. This Check works by going through all n_grams in the news title with n = length of the company string and calculating the levenshtein distance 
5. The "match" and all its corresponding attributes and the confidence score get written as a document into elastic search.
6. We will use this dataset for further visualizations


## How2Run (without importing the corporate-event-dump)
1. `cd iit_integrator`
2. `pip install .`
3. `python main.py`
