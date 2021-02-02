from reviewminer.core import *

import pandas as pd
import reviewminer as rm

reviews_df = pd.read_csv("./reviews.csv")
print("comment" in reviews_df.columns)



rm = ReviewMiner(reviews_df.head(100), 'id', 'comments')

print(rm.negative_comments_view())

#isinstance(rm.return_negative_comments_of_aspect('bed'), list) is True

# rm.aspect_opinon_for_all_comments()
# rm.overall_sentiment(_testing=True)

#rm.id_column = 1
#rm._examine_id_column(1)


# rm.one_time_analysis()

# rm.aspect_opinon_for_all_comments()
# print(rm.top_aspects)



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









