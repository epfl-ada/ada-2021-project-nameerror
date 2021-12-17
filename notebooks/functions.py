"Some helpful functions"

import re

import pandas as pd
import numpy as np

from scipy.stats import ttest_ind

# Visualization
from matplotlib import pyplot as plt

# NLP
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def list_to_str(data, col_names):
    """conversion of list values to string values for convenience"""
    for col_name in col_names:
        data[col_name] = data[col_name].str[0]

def get_sentiment(analyzer, sentence):
    """Performs sentiment analysis of the sentence using the analyzer and
    returns a corresponding textual label of the sentiment
    """
    THRESHOLD = 5e-2
    compound = analyzer.polarity_scores(sentence)['compound']
    if compound > THRESHOLD:
        return 'positive'
    elif compound < -THRESHOLD:
        return 'negative'
    else:
        return 'neutral'

def timestamp_to_datetime(date_str):
    """
    Convert Wikidata timestamp to datetime format.
    """
    match = re.findall('\d{4}-\d{2}-\d{2}', date_str)[0]
    match = re.split('-00', match, 1)[0]
    return pd.to_datetime(match, errors='coerce')

def get_domain(url):
    """getting domain of an url"""
    r = tldextract.extract(url)
    return f"{r.domain}.{r.suffix}"

def process_missing_values(df, column_name):
    df[column_name].replace('None', np.nan, inplace=True)
    
def handle_wikidata_multidates(df, attr_name):
    """Takes care of entries of the column in wikidata datetime timestamp 
    and having multiple column values, picks first and converts it to datetime format.
    The function is specifically designed for birthdates as it was noticed that some
    entries have values close to each, and slight time differences in these values
    does not affect the analysis in any meaningful way as it is done on much larger time 
    interval.
    """
    df[attr_name] = df[attr_name].apply(
        lambda dates: None if dates is None or len(dates) == 0\
                            else timestamp_to_datetime(dates[0]))

def preprocess_dataframe(df, handle_birth_dates=False):
    """Converts certain columns to required types for easier handling,
    drops duplicates and marks missing values to be recognized by pandas.
    handle_birth_dates argument added for backcompatibility.
    """
    df['date'] = pd.to_datetime(df['date'])
    df.drop_duplicates(subset='quoteID', keep='first', inplace=True)
    process_missing_values(df, 'speaker')
    if handle_birth_dates:
        handle_wikidata_multidates(df, 'date_of_birth')

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

def get_top_entries(df, attr_name, cutoff_count=-1, top_k=-1):
    """Gets most frequest values of attribute attr_name in the given dataframe as
    a list sorted by how frequent they are descendingly. Parameter cutoff_count
    offers flexibility so all values that occur less than cutoff_count times can be 
    ignored in the return result. If top_k is > 0 it will ensure that 
    the result is no longer than top_k elements
    """
    top_values = df[attr_name].dropna()\
            .explode()\
            .value_counts(sort=True)
    if cutoff_count > 0:
        mask = top_values >= cutoff_count
        top_values = top_values[mask]
    result = list(top_values.index)
    if top_k > 0:
        result = result[:top_k]
    return result

def get_multivalue_col_mask(df, attr_name, value):
    """Returns mask that tells whether respective rows have the specified value
    in the given multivalue column attr_name for the given dataframe.
    """
    return df[attr_name].apply(lambda values: values is not None and value in values)

def show_mean_with_sem(ax, x, y_mean, y_sem, color, alpha=.2):
    """Plots mean together with its sem in matching colors in the given plot"""
    ax.fill_between(x, y_mean - y_sem, y_mean + y_sem, color=color, alpha=alpha)
    ax.plot(x, y_mean, c=color)

def perform_hypothesis_testing_of_means(distribution_1, distribution_2):
    """Performs Welch's t-test and Standard independent 2 sample test to test equality
    of the expected values of the given distributions and prints p-values to stdout
    """
    _, standard_pvalue = ttest_ind(distribution_1, distribution_2, equal_var=True)
    _, welch_pvalue = ttest_ind(distribution_1, distribution_2, equal_var=False)

    # Value of Welch's t-test is used for conclusion as it doesn't rely on any assumptions
    conclusion = 'unlikely' if welch_pvalue < 5e-2 else 'undecidable'
    print(f' ----| Standard independent 2 sample test p-value: {standard_pvalue}')
    print(f' ----| Welch’s t-test p-value: {welch_pvalue}')
    print(f' ====> Conclusion: The equality of the expected values of the given distributions is [{conclusion.upper()}]')
    
def normalize(series):
    """Returns normalized version of the series"""
    smax = series.max()
    smin = series.min()
    return (series - smin) / (smax - smin)

def standardize(series):
    """Returns standardized version of the series"""
    return (series - series.mean()) / series.std()

def multi_hot(df, attr_name, cutoff):
    """Multihot encoding of the given attribute of the dataframe while 
    keeping only values appearing at least cutoff time. If no values made through
    cutoff the result is None
    """
    values = get_top_entries(df, attr_name, cutoff_count=cutoff)
    if len(values) == 0:
        return None
    return pd.concat([
        get_multivalue_col_mask(df, attr_name, value).astype(int).rename(f'{attr_name}_{value}')\
        for value in values
    ], axis=1)