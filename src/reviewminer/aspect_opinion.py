from textblob import TextBlob
from src.reviewminer.basic import *
import nltk
# nltk.download('brown')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


class AspectOpinionExtractor(Reviews):

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
                 sentence_blob):
        """
        Extract the adverb or adjective;
        Judge whether the index-th word in sentence_blob is an adverb or adjective

        :param index: the index (x-th item in word_list)
        :param word_list: a list of words
        :param sentence_blob: a TextBlob object
        """
        if self.valid(index, sentence_blob):
            if sentence_blob.tags[index][1] in ['RB', 'RBR', 'RBS', 'JJ', 'JJR', 'JJS']:
                word_list.append(sentence_blob.tags[index][0])

    def extract_attributes_pref(self,
                                aspect: str,
                                first_word_index: int,
                                sentence_blob) -> str:
        """
        Extract the attributes that are right before the aspect in the sentence;
        We look at no more than 2 words before;

        e.g. "very nice coffee" --> {'coffee': 'very nice'}
             "weather was perfect, the coffee ..." --> {'coffee': ''}
             "friendly staff" --> {'staff': 'friendly'}

        :param aspect:
        :param first_word_index: the index of the first word in the aspect in the sentence
        :param sentence_blob:
        :return:
        """
        pref_words = []

        self.add_word(first_word_index - 1, pref_words, sentence_blob)

        # only when there's a adj/adv one index before the aspect will we look at the work 2 indexes before
        if len(pref_words) > 0:
            self.add_word(first_word_index - 2, pref_words, sentence_blob)

        return ' '.join(pref_words)
