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

# Performs sentiment analysis of the sentence using the analyzer and
#    returns a corresponding textual label of the sentiment
def get_sentiment(analyzer, sentence):
    THRESHOLD = 5e-2
    compound = analyzer.polarity_scores(sentence)['compound']
    if compound > THRESHOLD:
        return 'positive'
    elif compound < -THRESHOLD:
        return 'negative'
    else:
        return 'neutral'

# Converts date from the format found on Wikidata to the one used by pandas
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

# getting domain of an url
def get_domain(url):
    r = tldextract.extract(url)
    return f"{r.domain}.{r.suffix}"

def processMissingValues(df, column_name):
    df[column_name].replace('None', np.nan, inplace=True)

def preprocess_dataframe(df):
    df['date'] = pd.to_datetime(df['date'])
    df.drop_duplicates(subset='quoteID', keep='first', inplace=True)
    processMissingValues(df, 'speaker')

def plot_sentiment_attribute_percentage(df, attr_name, ax):
    sentiment_attr_counts = df[['sentiment', attr_name]]\
        .pivot_table(index='sentiment', columns=attr_name, aggfunc=len)\
        .replace(np.NaN, 0)

    sentiment_attr_percentages = sentiment_attr_counts / sentiment_attr_counts.sum(axis=0)
    sentiment_attr_percentages.plot.bar(ax=ax)
    
def extend_with_sentiment_polarity_scores(df, text_attr_name='quotation'):
    """Calculates VADER polarity scores and adds them to each row of the given 
    dataframe as columns neg, neu, pos and compound.
    """
    vader = SentimentIntensityAnalyzer()
    return pd.concat([
        df,
        pd.DataFrame.from_records(
            df[text_attr_name].apply(lambda sentence: vader.polarity_scores(sentence))
        )
    ], axis=1)

def group_by_date_col(df, date_col, freq):
    """Groups df by the given date column for the given frequency 
    without altering the index of the original dataframe. Important
    to note that the function creates a shallow copy of the dataframe 
    to perform this operation
    """
    df_copy = df.copy(deep=False)
    df_copy.index = df_copy[date_col]
    return df_copy.groupby(pd.Grouper(freq=freq))
