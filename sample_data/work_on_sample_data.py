from src.reviewminer.basic import *
from src.reviewminer.aspect_opinion import *

import pandas as pd

reviews_df = pd.read_csv("reviews.csv")

aoe = AspectOpinionExtractor()

print(aoe.aspect_extractor("Orange juice is healthier than and hot coffee"))

