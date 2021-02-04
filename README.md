# ReviewMiner 

[![PyPI version](https://badge.fury.io/py/reviewminer.svg)](https://badge.fury.io/py/reviewminer)
[![Build Status](https://travis-ci.org/tianyiwangnova/2021_project__ReviewMiner.svg?branch=main)](https://travis-ci.org/tianyiwangnova/2021_project__ReviewMiner)
[![codecov](https://codecov.io/gh/tianyiwangnova/2021_project__ReviewMiner/branch/main/graph/badge.svg?token=X8OKTSU13D)](https://codecov.io/gh/tianyiwangnova/2021_project__ReviewMiner)

`ReviewMiner` is built for **analyzing customer reviews, or any text datasets that are similar to review data *(short opinions 
collected from multiple individuals)* **. The package is built on top of a variety of natural language processing packages ---- 
`nltk`, `TextBlob` and `gensim`. The purpose is to allow users to run multiple common text analysis on the review data 
at one time, providing intuitive visualizations that can help the users uncover insights, and intermediate output tables that can be used for
further investigations. 

Features:
* **Aspect and opinion extraction** The key methodology in this package is aspect-based opinoin mining. The package has 
its own algorithm to extract aspects and the relative opinion words from the review data. 
* **Sentiment on comment and aspect level** The package can offer sentiment scores on both comment level and aspect level
* **Negative reviews investigation** The users can quickly check the negative sentences in the comments. They can also 
investigate negative comments about certain aspects

## Installation
```
$ pip install reviewminer
```

## Quickstart

#### One-stop text analysis
```python
import reviewminer as rm
import pandas as pd

# read our sample data
reviews_df = pd.read_csv("https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/"
                                 "sample_data/reviews.csv")

# create a reviewminer object (for an example, we will just use the first 500 rows in the data
sample_rm = rm.ReviewMiner(reviews_df.head(500), id_column="Id", review_column='Text')

# run the one time analysis and you will see 
sample_rm.one_time_analysis()
```

The function will print out 4 visualizations:

* Popular aspects and opinions
![popular](https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/sample_data/popular_aspects_example.png)

This chart displays 9 most common aspects found in the reviews and the most popular opinions words people used to 
describe them. In each bar chart, the heights show the percentages of the people using the each opinion word.

* Distribution of sentiment scores of all comments
![sentiment](https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/sample_data/sentiment_score_example.png)

* Radar chart of the most common aspects and their average sentiment scores
![radar](https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/sample_data/radar_chart_example.png)

* Aspects with the most negative comments
![negative](https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/sample_data/aspects_negative_example.png)

#### Exclude certain aspects

You might want to exclude some aspects. For example, the aspect "everything" can't quite offer valuable insights. 
Then you can do this:
```python
sample_rm.aspect_mute_list = ['everything']
sample_rm.popular_aspects_view()
```
You will see that the aspect "everything" disappears from the most common aspect list.














