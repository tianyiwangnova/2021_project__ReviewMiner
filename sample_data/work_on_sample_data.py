from src.reviewminer.core import *

import pandas as pd

class CustomError(Exception): pass

#from src.reviewminer.core import AspectOpinionExtractor

reviews_df = pd.read_csv("reviews.csv")

re = Reviews(reviews_df)



#aoe = AspectOpinionExtractor(reviews_df, 'id', 'comments')

#print(aoe.id_column)

#print(aoe.aspect_extractor("I love drinking orange juice."))
#print(aoe.aspect_extractor("Orange juice is healthier than and hot coffee"))

