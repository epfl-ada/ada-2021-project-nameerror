# Understanding Vegetarianism and Veganism Through the Media

## Abstract
We have been hearing more and more about the problems related to meat (health, environment, ethics) for some time. It is in this context that several movements (vegetarianism, veganism) have started to become popular. In this project we want to understand the evolution of vegetarianism and veganism by looking at news quotes from the last decade. We aim to extract the general opinion of the media about vegetarianism and see the evolution in time. Furthermore the motivations and characteristics of the speakers who talk about these movements will be analyzed. We will focus on these two movements because they are the most important and popular. In the following when we talk about vegetarianism we also include veganism since it is a subset of vegetarianism.

## Research questions
In this project we will address the following questions.

### Question 1: How did vegetarianism evolve since 2008?
We would like to explore the evolution of the movement through time. In other words, we will observe the frequency of appearance of the terms related to vegetarianism in the media for each year and see if there is indeed a media coverage increase since 2008.

To complete this analysis, it will also be necessary to group the selected quotes according to the positive or negative opinion of the media about this diet. In particular, quotes expressing the benefits of vegetarianism will be grouped together. This clustering will be done for each year.

### Question 2: Who are the individuals for and against vegetarianism?
In this section we will try to group speakers according to their feelings about vegetarianism or veganism. The speakers who are for the movement will belong to one group whereas the individuals who are against will belong to the other group. We will then analyze the characteristics (age, gender, nationality, and so on) of the people in each group. This will be done for each year since 2008. 

### Question 3: What are the motivations behind vegetarianism/veganism?
By selecting quotes that contain terms related to areas such as ethics, environment or health and terms that relate to vegetarianism or veganism we can see in which context these movements tend to appear the most. Do the media talk more about vegetarianism in relation to health, environment or ethics? It allows us to have a glimpse at the motivations behind these diets.

## Methods and datasets
To answer our questions we will use the Quotebank dataset for citation-speaker pairs. It will then be necessary to enrich this dataset with metadata about the speakers that we will obtain from the Wikidata knowledge base. 
The most difficult part in this project is to group the selected quotations according to the sentiment. A quotation which is against a topic is more likely to contain negative overall feeling/sentiment whereas a quotation talking about the benefits of a topic is expected to have a more positive feeling. This task requires a sentiment analysis of the quotations. We will use [VADER](https://www.nltk.org/_modules/nltk/sentiment/vader.html) (Valence Aware Dictionary and sEntiment Reasoner) which is an open-source sentiment analyzer pre-build library to achieve this. The results will be used as an additional feature in our dataset. 

This will be done for each year since 2008 to get one dataset per year with the following features: quoteID, quotation, speaker, qids, date, numOccurrences, probas, urls, phase, speaker_qid, gender, nationality, date_of_birth, ethnic_group, occupation, party, academic_degree, domains, sentiment. From there we will merge the datasets from each year into one final enriched dataset. From there we will be able to acquire all the required statistics to answer our questions.

[Flair](https://github.com/flairNLP/flair) also helps us on several aspects, including tagging. Indeed, it permits us to add tags to tokens from our quotations, such as organizations, locations, persons, events, products, and more. We use pre-trained sequence tagger models like “ner” or “ner-ontonotes”. These tags can be linked with many other results from other parts, such as events and trendings, or products and political parties.

As for our GitHub repository we have the following organization:
* [dictionary_extending.ipynb](notebooks/dictionary_extending.ipynb) - This notebook contains code to explore useful keywords for the selection of quotations related to vegetarianism/veganism performed by looking at most relevant Google search pages on these topics
* [filter_dataset.ipynb](notebooks/filter_dataset.ipynb) - This notebook selects the quotations related to vegetarianism/veganism from the Quotebank dataset
* [enrich_dataset.ipynb](notebooks/enrich_dataset.ipynb) - This notebook contains the code to build the dataset from the Quotebank dataset and the Wikidata knowledge base. There is also the code to merge the datasets from different years
* [analysis.ipynb](notebooks/analysis.ipynb) - This notebook contains basic exploratory analyses as well as deeper look into data on the final dataset of the year 2020

The order is the same as our pipeline, that is keyword selection, quotation selection, data augmentation and merging and analysis. This was done mainly for the year 2020 as a proof of feasibility. The extension to other years follows a similar pattern.

The final data story is planned to be presented in a form of a webpage and for this purpose we plan to mainly use bootstrap for design, jquery for functionality and d3 for static and dynamic visualisations out of external tools. Possibly additional tools may be needed and used as well.

## Organization and timeline
For the first milestone we are going to work together to obtain a clean dataset containing the selected quotations merged with the speaker attributes and sentiments for all years. From there the work will be divided by research questions. The distribution of the tasks is as follow:
* Question 1 - Romain Wiorowski
* Question 2 - Klavdiia Naumova and Alexandre Tkatch
* Question 3 - Milos Vujasinovic

The timeline will be organized around the following milestones:
* Milestone 1 (21.11.2021) - Prepare the final dataset of the selected quotes merged with the speaker attributes and sentiments for the years.
* Milestone 2 (30.11.2021) - Make all the required visualizations and compute the required statistics.
* Milestone 3 (10.12.2021) - Putting everything together, selecting the relevant information for the data story. Finishing the first draft.  
* Milestone 4 (17.12.2021) - Working on the final details, making everything beautiful and readable.

## Questions for TAs
* We thought about creating some baseline statistics from randomly sampling the Quotebank dataset to make our conclusion more robust. Is this a viable solution?
