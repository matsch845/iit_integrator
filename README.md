# integrator

## general architecture
Step 0: we imported the crawl set of RB into elastic via incorporate-event-import.py

After that main.py retrieves our google news data and the RB data from elastic search and runs our matcher (integrator "matcher_strict")

The integrator works this way:
1. It takes the information of RB crawl and finds the company in the string via regex. (depending on where the company is written)
2. It cleans the company string and sets the fitting n_gram amount depending on the token count in the company string.
3. It takes the google news headline and cleans it.
4. It splits the clean headline into the corresponding amount of tokens (depnding on those of the company string)
5. It calculates token_based and edit distance for all n amount of adjacent tokens in the headline vs. the company string
6. In case the distances reach a certain threshold it calls it a match and calculates a confidence score: how confident are we in that match?
7. The "match" and all its corresponding attributes and the confidence score get written as a document into elastic search.

We choose a threshold wich will lead to some arbitrary matches but we can filter over the confidence score to select real, confident matches via making the matching stricter.

In case of short company strings the matcher will have some issues, and maybe think there is a match when there is not. For those cases the confidence score got introduced, and will be used for further analysis.


## how2run
1. `python main.py`
