This milestone proposes three ideas ordered in increasing difficulty. All ideas are intended to be performed on phase E data. The ideas take an advantage of nouns and named entities in a quote
which have to be extracted. This could be performed using Part-of-Speech tagging and Named Entity Recognition respectively. 

# Ideas

- We could use the quotes to create a small historic overview of the past years. Events are characterized by their spike in popularity
so that’s what we look for. We count occurrences of each term (i.e. noun/named entity) grouped by month, and calculate the difference between a month and the previous for each term and available month. Finally for each available month we select few terms with
the highest difference and create a small timeline to display them. 

- Targeting tools have proven their value time and time again. Quotebank can be exploited for this purpose, to specifically target different professions. The idea is to select a term (i.e.
noun/named entity) and have a program return a list of professions that are most interested in the term. For each quote we associate the occupation(s) of the most probable speaker with the quote by cross-referencing Wikidata using the speaker identifier available
in Quotebank. When a term is entered we filter out all quotes that doesn’t include the term and count the number of distinct speakers of each occupation/profession that are associated with the remaining quotes. As there is different numbers of speakers of each
profession, we would only report the percent of the speakers of each profession that are interested in the term. This could be used to guide a client’s decisions (e.g. a president) based on the professions that particularly value their opinions and actions.
With addition of sentiment analysis this could be an even more powerful tool. 

- Quotebank could be attempted to be used to group speakers based on their interest in similar topics. We would first create a word embedding space from the set of all quotes we have.
Next, we would attempt to embed the quotes in the same space. A way to achieve this would be to extract important terms (for simplicity this will be nouns and named entities) from a quote and take their average in the embedding space weighted by their number
of occurrences in the quote to get the embedding of the given quote. Terms that are over or underrepresented in the corpus would be ignored to avoid their presumably negative impact on the result. In the next step we would embed each speaker by taking an average
of the quotes they are assumed to have said weighted by the probability that the speaker has said the given quote. Afterwards, we would select only top N speakers by the number of quotes in the corpus. Finally, we could either do clustering on the selected
speakers and report the results in form of a table or perform PCA from the embedding space to 2D on the selected speakers, followed by clustering and visualize the results for better reader experience.



#### Remarks by a TA

- Lack of questions aimed to be answered with these ideas
