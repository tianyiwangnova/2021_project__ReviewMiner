# ReviewMiner 

[![PyPI version](https://badge.fury.io/py/reviewminer.svg)](https://badge.fury.io/py/reviewminer)
[![Build Status](https://travis-ci.org/tianyiwangnova/2021_project__ReviewMiner.svg?branch=main)](https://travis-ci.org/tianyiwangnova/2021_project__ReviewMiner)
[![codecov](https://codecov.io/gh/tianyiwangnova/2021_project__ReviewMiner/branch/main/graph/badge.svg?token=X8OKTSU13D)](https://codecov.io/gh/tianyiwangnova/2021_project__ReviewMiner)

`reviewminer` is built for **analyzing customer reviews, or any text datasets that are similar to review data _(short opinions 
collected from multiple individuals)_**. It is built on top of `nltk` and `TextBlob`. 
`reviewMiner` takes the pain out of learning NLP packages and building analytics pipelines from scratch. It provides a handy tool 
for the users to quickly organize reviews data into digestible insights. 

Features:
* **Aspect and opinion extraction** The key methodology in this package is aspect-based opinoins mining. The package has 
its own algorithm to extract aspects and the related opinion words from the review data. 
* **Sentiment on comment and aspect level** The package can offer sentiment scores on both comment level and aspect level
* **Negative reviews investigation** The users can quickly display the negative sentences in the comments. They can also 
investigate negative comments by aspects.

## Useful Links

* [Knowledge Center](https://github.com/tianyiwangnova/2021_project__ReviewMiner/wiki/Knowledge-Center)
* [Documentation](https://github.com/tianyiwangnova/2021_project__ReviewMiner/wiki/Documentation)

## Installation
```
$ pip install reviewminer
```

## Quickstart

### One-stop text analysis

We use the [Women’s Clothing E-Commerce dataset](https://www.kaggle.com/nicapotato/womens-ecommerce-clothing-reviews) on Kaggle to run the examples. 

```python
import reviewminer as rm
import pandas as pd

# read our sample data
reviews_df = pd.read_csv("https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/sample_data/Womens%20Clothing%20E-Commerce%20Reviews.csv")

# create a reviewminer object 
sample_rm = rm.ReviewMiner(reviews_df, id_column="Id", review_column='Text')

# run the one time analysis and you will see 
sample_rm.one_time_analysis()
```

The function will print out 4 visualizations:

* **Popular aspects and opinions**
![popular](https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/sample_data/popular_aspects_example.png)

This chart displays 9 most common aspects found in the reviews and the most popular opinions words people used to 
describe them. In each bar chart, the heights show the percentages of the people using the each opinion word.

* **Distribution of sentiment scores of all comments**
![sentiment](https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/sample_data/sentiment_score_example.png)

* **Radar chart of the most common aspects and their average sentiment scores**
![radar](https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/sample_data/radar_chart_example.png)

From this chart you can quickly compare customers' average sentiment on each of the common aspects. Here "size" seems to be an aspect that customers are not quite satisfied with.

* Aspects with the most negative comments
![negative](https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/sample_data/aspects_negative_example.png)

### Exclude certain aspects

You might want to exclude some aspects. For example, if you don't want the aspect "colors", you can do the following:
```python
print("Before:", sample_rm.top_aspects)
sample_rm.aspect_mute_list = ['colors']
print("After:", sample_rm.top_aspects)
```
![exclude](https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/sample_data/top_aspects_example.png)

When aspect_mute_list has changed, the visualizations will change as well when the related methods are calling, but the 
base intermediate output tables (e.g. aspect_opinion_df) won't change.

### Check out negative comments of an aspect

From the radar chart above we saw that customers might not be very satisfied with "sizes" of the clothes. Let's check out the negative comments around "size"
```python
sample_rm.negative_comments_by_aspects_dict['size']
```
![size](https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/sample_data/negative_sentences_example.png)

### Check out the most common opinion words of an aspect

```python
sample_rm.single_aspect_view("material")
```

### Radar chart of average sentiments for a list of aspects

```python
sample_rm.aspects_radar_plot(['shirt','skirt','sweater','blouse','jacket','dress'])
```
![radar_customized](https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/sample_data/radar_chart_customized_example.png)

## Tips

* It’s better to feed in review data on a specific product or service. If you only run it on the review data for a specific 
ramen restaurant, for example, it’s easier to find meaningful aspects. If you feed in amazon reviews for 5 totally different
 products, the result might not be very meaningful.
 
* Sometimes a sample of the data can tell the whole story. If you have a million reviews for the unibet app, for example, 
the result will be very similar to the result you get from a random sample of 10k reviews. So don’t rush to feed all your 
data in, try with a sample first ;)














