from src.reviewminer.basic import *


from src.reviewminer.aspect_opinion import *
from src.reviewminer.sentiment import *
from src.reviewminer.core import *

import pandas as pd

reviews_df = pd.read_csv("./reviews.csv")

#rm = ReviewMiner(reviews_df.head(100), 'id', 'comments')
rm = ReviewMiner()
rm.df = 1
print(rm.df)
rm.one_time_analysis()

#print(ss.sentiment_for_one_comment(ss.df.iloc[10,1]))




# aoe = AspectOpinionExtractor(reviews_df.head(100), 'id', 'comments')
# aoe.aspect_opinon_for_all_comments()
# aoe.popular_aspects_view()
# #aoe.single_aspect_view("room")
#aoe.single_aspect_view("room", num_top_words=5, xticks_rotation=30)



# print(aoe.most_popular_opinions("room", 5))
#
# sample_df = pd.DataFrame({
#         'id': [100, 101, 102, 103],
#         'comments': ['The room is comfortable. The room is spacious.',
#                     'The sunny room is very spacious.',
#                     'The spacious room is sunny',
#                     'The spacious room is sunny. The beautiful room is comfortable']})
#
# aoe = AspectOpinionExtractor(sample_df, 'id', 'comments')
# aoe.aspect_opinon_for_all_comments()
# print(len(aoe.df_with_aspects_opinions.loc[0, "aspects_opinions"]))
# print(aoe.df_with_aspects_opinions)
#
# aoe.aspect_opinon_for_all_comments()
# print(aoe.most_popular_opinions("room"))









