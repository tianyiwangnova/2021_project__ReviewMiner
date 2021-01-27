from textblob import TextBlob
from src.reviewminer.basic import *
import nltk
import datetime

nltk.download('brown')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


class AspectOpinionExtractor(Reviews):

    """
    Extract aspects and opnions from the reviews data
    """

    def __init__(self,
                 df: pd.DataFrame = None,
                 id_column: str = None,
                 review_column: str = None):
        """
        Take a data frame where each row is a comment/review

        :param df: a data frame where each row is a comment/review; The data frame should have at least an ID column
                   that stores the unique IDs of the comments, and a review column where the actual comments/reviews
                   are stored
        :param id_column: the name of the column that stores the unique IDs of the comments
        :param review_column: the name of the column where the actual comments/reviews are stored
        """
        Reviews.__init__(self, df=df, id_column=id_column, review_column=review_column)

    @staticmethod
    def aspect_extractor(sentence: str) -> list:
        """
        Extract aspects (noun phrases and nouns) from a sentence

        :param sentence: a sentence
        :return: a list of aspects in the sentence
        """
        sentence = sentence.lower()
        sentence_blob = TextBlob(sentence)

        # extract noun phrases
        # e.g. "I love drinking orange juice" --> "orange juice"
        noun_phrases = sentence_blob.noun_phrases

        # extract nouns
        # NN: noun; NNS noun plural; NNP: proper noun, e.g. "Harris"; NNPS: proper noun plural
        nouns_1 = [n for n, t in sentence_blob.tags if t in ['NN', 'NNS', 'NNP', 'NNPS']]

        # delete nouns that are actually part of the noun phrases
        nouns_2 = []

        if len(nouns_1) == 1:
            nouns_2 = nouns_1

        if len(nouns_1) > 1:
            for i in range(len(nouns_1)):
                if i == 0 and ' '.join([nouns_1[i].lower(), nouns_1[i + 1].lower()]) not in noun_phrases:
                    nouns_2.append(nouns_1[i])
                if 0 < i < len(nouns_1) - 1 \
                        and ' '.join([nouns_1[i - 1].lower(), nouns_1[i].lower()]) not in noun_phrases \
                        and ' '.join([nouns_1[i].lower(), nouns_1[i + 1].lower()]) not in noun_phrases:
                    nouns_2.append(nouns_1[i])
                if i == len(nouns_1) - 1 and ' '.join([nouns_1[i - 1].lower(), nouns_1[i].lower()]) not in noun_phrases:
                    nouns_2.append(nouns_1[i])

        # merge the results
        candidate_aspects = noun_phrases + nouns_2
        candidate_aspects = [a for a in candidate_aspects if a != 'i']

        return candidate_aspects

    @staticmethod
    def valid(x: int, sentence_blob: TextBlob) -> bool:
        """
        Check whether an index(x) is valid

        :param x: an integer
        :param sentence_blob: a Textblob object
        :return: bool
        """
        return True if 0 <= x < len(sentence_blob.tags) else False

    @staticmethod
    def merge_two_dicts(dict1: dict, dict2: dict) -> dict:
        """
        {'a': 'apple', 'b': 'boy'}
        {'a': 'air', 'c': 'cat'}
        ==> {'a': 'apple air', 'b': 'boy', 'c': 'cat'}

        :param dict1: the first dictionary
        :param dict2: the second dictionary
        :return: merged dictionary
        """
        for k in dict2:
            if k not in dict1:
                dict1[k] = dict2[k]
            elif k in dict1:
                dict1[k] = ' '.join([dict1[k], dict2[k]])
        return dict1

    @staticmethod
    def has_aspect(dict_string: str, aspect: str) -> bool:
        """
        Check whether an aspect (a string) is in the keys of a dictionary (the dictionary is in string format like
        "{'a': 'apple', 'b': 'boy'}"

        :param dict_string: a dictionary in string (e.g. "{'a': 'apple', 'b': 'boy'}")
        :param aspect: an aspect
        :return: bool
        """
        aspects = list(eval(dict_string).keys())
        return True if aspect.lower() in aspects else False

    @staticmethod
    def has_opinion(dict_string: str, aspect: str, opinion: str) -> bool:
        """
        Check whether an aspect has an opinion
        e.g. "{'building':'tall beautiful magnificent', 'music':'classic pop calm'}" -->
        The aspect "building" has the opinion word "tall" but it doesn't have the opnion word "pop"

        :param dict_string: a dictionary in string (e.g. "{'a': 'apple', 'b': 'boy'}")
        :param aspect: an aspect (a word)
        :param opinion: an opnion (a word)
        :return: bool
        """
        opinions = eval(dict_string)[aspect].lower().split()
        return True if opinion.lower() in opinions else False

    def is_be(self, x: int, sentence_blob: TextBlob) -> bool:
        """
        Check whether the word (sentence_blob[x]) is one of ['am','is','are','was','were']

        :param x: the index (x-th item in sentence_blob)
        :param sentence_blob: a TextBlob object
        :return: bool
        """
        return True if self.valid(x, sentence_blob) and sentence_blob.words[x].lower() in ['am', 'is', 'are', 'was',
                                                                                           'were'] else False

    def add_word(self,
                 index: int,
                 word_list: list,
                 sentence_blob) -> list:
        """
        Extract the adverb or adjective;
        Judge whether the index-th word in sentence_blob is an adverb or adjective;
        The word "very" is not counted

        :param index: the index (x-th item in word_list)
        :param word_list: a list of words
        :param sentence_blob: a TextBlob object
        :return: the enriched word list
        """
        if self.valid(index, sentence_blob):
            if sentence_blob.tags[index][1] in ['RB', 'RBR', 'RBS', 'JJ', 'JJR', 'JJS'] and \
                    sentence_blob.tags[index][0].lower() != 'very':
                word_list.append(sentence_blob.tags[index][0].lower())
        return word_list

    def extract_attributes_pref(self,
                                first_word_index: int,
                                sentence_blob) -> str:
        """
        Extract the attributes that are right before the aspect in the sentence;
        We look at no more than 2 words before;
        Only when there's a adj/adv one index before the aspect will we look at the work 2 indexes before;

        e.g. "delicious warm coffee" --> {'coffee': 'warm delicious'}
             "weather was perfect. The coffee ..." --> {'coffee': ''}
             "Very friendly staff" --> {'staff': 'friendly'}

        :param first_word_index: the index of the first word in the aspect in the sentence
        :param sentence_blob: the sentence blob where the aspect locates
        :return: the attributes of the aspect in a string (words are seperated by ' ')
        """
        pref_words = []

        pref_words = self.add_word(first_word_index - 1, pref_words, sentence_blob)

        # only when there's a adj/adv one index before the aspect will we look at the work 2 indexes before
        if len(pref_words) > 0:
            self.add_word(first_word_index - 2, pref_words, sentence_blob)

        return ' '.join(pref_words)

    def extract_attributes_suff(self,
                                ca_last_index: int,
                                sentence_blob) -> str:
        """
        Extract the attributes that are right after the aspect + 'be' in the sentence;
        We look at no more than 2 words after;
        When there's a "not" or "n't" before the adv or adj, we will combine the negation word with the adv/adj

        e.g. "coffee was very nice" --> {'coffee': 'nice'}
             "We had coffee. The delicious desert...." --> {'coffee': ''}
             "The cafe is beautiful. The coffee.." --> {'cafe': 'beautiful'}
             "the bed was not comfortable" --> {'bed': 'notcomfortable'}

        :param ca_last_index: the index of the last word in the aspect in the sentence
        :param sentence_blob: the sentence blob where the aspect locates
        :return: the attributes of the aspect in a string (words are seperated by ' ')
        """
        suff_words = []

        # the adj/adv must come after the "be noun"
        if self.is_be(ca_last_index + 1, sentence_blob):
            suff_words = self.add_word(ca_last_index + 2, suff_words, sentence_blob)

        # only when there's a qualified adj/adv 2 index after the aspect will we look at the word 3 indexes after
        if len(suff_words) > 0:
            suff_words = self.add_word(ca_last_index + 3, suff_words, sentence_blob)

        # or if the word after 'be' is very, we will look at the word 3 indexes after
        if sentence_blob.tags[ca_last_index + 2][0].lower() == 'very':
            suff_words = self.add_word(ca_last_index + 3, suff_words, sentence_blob)

        attr = ' '.join(suff_words)
        if len(suff_words) == 2 and suff_words[0] in ['not', "n't"]:
            attr = ''.join(suff_words)

        return attr

    def opinion_extractor(self,
                          candidate_aspects: list,
                          sentence_blob) -> dict:
        """
        Extract the aspects and opinions associated with them in a sentence; returns a dictionary

        :param candidate_aspects: a list of aspects for extracting their opinions
        :param sentence_blob: the TextBlob object of the sentence that we are analyzing
        :return: a dictionary with the aspects as keys and the opinions wrapped up as a single string of words
                 seperated with ' ' e.g. {'bedroom': 'sunny spacious', 'wardrobe': 'beautiful'}
        """
        candidate_aspects_dict = {}
        aspect_opinion_dict = {}

        if len(candidate_aspects) > 0:
            for a in candidate_aspects:
                try:
                    candidate_aspects_dict[a] = {}
                    first_word_index = sentence_blob.words.index(a.split()[0])  # index of the first word of the aspect
                    last_word_index = sentence_blob.words.index(a.split()[-1])  # index of the last word of the aspect
                    # extract the attributes that appear before the aspect in the sentence
                    aspect_opinion_dict[a] = self.extract_attributes_pref(first_word_index, sentence_blob)
                    # extract the attributes that appear after the aspect in the sentence
                    aspect_opinion_dict[a] = ' '.join(
                        [aspect_opinion_dict[a], self.extract_attributes_suff(last_word_index, sentence_blob)])
                except:
                    pass

        return aspect_opinion_dict

    def aspect_opinion_for_one_comment(self, sentence: str) -> dict:
        """
        Extract aspects and opinions for one sentence

        :param sentence: the sentence for analyzing
        :return: a dictionary with the aspects as keys and the opinions wrapped up as a single string of words
                 seperated with ' ' e.g. {'bedroom': 'sunny spacious', 'wardrobe': 'beautiful'}
        """
        sentence = str(sentence).lower()
        sentence_blob = TextBlob(sentence)
        candidate_aspects = self.aspect_extractor(sentence)
        aspect_opinion_dict = self.opinion_extractor(candidate_aspects, sentence_blob)

        return aspect_opinion_dict

    def aspect_opinon_for_all_comments(self, report_interval=500):
        """
        Extract aspects and opinions for all the comments in a pandas dataframe;

        :param report_interval:
        :return: a pandas dataframe with id, reviews and the string version of the aspect_opinion_dict
        """
        df = self.df.copy()
        id_column = self.id_column
        review_column = self.review_column

        begin = datetime.datetime.now()
        print("Aspect Opinion Extractor job begins: {}".format(begin))
        aspect_opinion_dict_all = {}  # a dictionary for all the aspects and opinions in the reviews data
        df_small = df[[id_column, review_column]].copy()
        df_small['aspects_opinions'] = ""  # add a new column for aspects and opinions in the comment

        for i in range(len(df)):
            d = self.aspect_opinion_for_one_comment(df_small.loc[i, review_column])
            aspect_opinion_dict_all = self.merge_two_dicts(aspect_opinion_dict_all, d)
            df_small.loc[i, 'aspects_opinions'] = str(d)
            if i % report_interval == 0 and i > 0:
                time_pass = (datetime.datetime.now() - begin).seconds / 60
                print("{:.2} min later: finished {:.2%}".format(time_pass, i / len(df)))

        aspects_opinions_df = pd.DataFrame(
            {'aspects': list(aspect_opinion_dict_all.keys()),
             'opinions': list(aspect_opinion_dict_all.values())}
        )

        aspects_opinions_df['opinions'] = aspects_opinions_df.opinions.str.strip()
        aspects_opinions_df['pop'] = aspects_opinions_df['opinions'].apply(len)
        aspects_opinions_df = aspects_opinions_df[aspects_opinions_df['opinions'] != ""]\
                              .sort_values(by=['pop'],
                                           ascending=False).drop('pop', 1)

        self.df_with_aspects_opinions = df_small
        self.aspects_opinions_df = aspects_opinions_df
