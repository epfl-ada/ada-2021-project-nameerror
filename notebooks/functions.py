"Some helpful functions"

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# conversion of list values to string values for convenience
def list_to_str (data, col_names):
    for col_name in col_names:
        data[col_name] = data[col_name].str[0]

# sentiment analysis
def get_sentiment(analyzer, sentence):
    THRESHOLD = 5e-2
    compound = analyzer.polarity_scores(sentence)['compound']
    if compound > THRESHOLD:
        return 'positive'
    elif compound < -THRESHOLD:
        return 'negative'
    else:
        return 'neutral'


# Source: https://stackoverflow.com/questions/49508986/how-to-convert-incomplete-and-bc-wikidata-dates-to-timestamp
def get_timestamp(date_str):
    # Probably not necessary
    date_str = date_str.strip()
    # Remove + sign
    if date_str[0] == '+':
        date_str = date_str[1:]
    # Remove missing month/day
    date_str = date_str.split('-00', maxsplit=1)[0]
    return pd.to_datetime(date_str)

# getting domain
def get_domain(url):
    r = tldextract.extract(url)
    return f"{r.domain}.{r.suffix}"
