from src.reviewminer.basic import *
from src.reviewminer.aspect_opinion import *

import pandas as pd

reviews_df = pd.read_csv("reviews.csv")

print(reviews_df.columns)

aoe = AspectOpinionExtractor(reviews_df.head(100), 'id', 'comments')

sentence1 = 'The weather is COOL'
sentence2 = "I ate eggs for breakfast"

aoe.aspect_opinon_for_all_comments()
print(aoe.df_with_aspects_opinions)
# print(aoe.extract_attributes_suff(1, TextBlob(sentence2)))

# candidate_aspects_dict = {}
# aspect_opinion_dict = {}
#
# a = 'coffee'
# sentence_blob = TextBlob(sentence2)
# print(sentence_blob.words)
# first_word_index = sentence_blob.words.index(a.split()[0])
# last_word_index = sentence_blob.words.index(a.split()[-1])
# aspect_opinion_dict[a] = aoe.extract_attributes_pref(first_word_index, sentence_blob)
# print(aspect_opinion_dict)








