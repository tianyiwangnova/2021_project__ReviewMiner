from src.reviewminer.core import *

import pandas as pd

from src.reviewminer.core import AspectOpinionExtractor

reviews_df = pd.read_csv("reviews.csv")
print(reviews_df.columns)

aoe = AspectOpinionExtractor(reviews_df, 'id', 'comments')

print(reviews_df.loc[1, "comments"], aoe.aspect_extractor(reviews_df.loc[2, "comments"]))
