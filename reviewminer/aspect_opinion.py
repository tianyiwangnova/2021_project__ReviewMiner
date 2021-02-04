import datetime
import matplotlib.pyplot as plt
import matplotlib.style as style
import seaborn as sns

import nltk
from nltk.tokenize import sent_tokenize
from textblob import TextBlob

from reviewminer.basic import *

nltk.download('brown')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

style.use('fivethirtyeight')
plt.rc('xtick', labelsize=20)
plt.rc('ytick', labelsize=20)


class AspectOpinionExtractor(Reviews):
    """
    Extract aspects and opinions from the reviews data
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

        return candidate_aspects

    @staticmethod
    def _valid(x: int, sentence_blob: TextBlob) -> bool:
        """
        Check whether an index(x) is valid

        :param x: an integer
        :param sentence_blob: a Textblob object
        :return: bool
        """
        return True if 0 <= x < len(sentence_blob.tags) else False

    @staticmethod
    def _merge_two_dicts(dict1: dict, dict2: dict) -> dict:
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
    def _has_aspect(dict_string: str, aspect: str) -> bool:
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
    def _has_opinion(dict_string: str, aspect: str, opinion: str) -> bool:
        """
        Check whether an aspect has an opinion
        e.g. "{'building':'tall beautiful magnificent', 'music':'classic pop calm'}" -->
        The aspect "building" has the opinion word "tall" but it doesn't have the opinion word "pop"

        :param dict_string: a dictionary in string (e.g. "{'a': 'apple', 'b': 'boy'}")
        :param aspect: an aspect (a word)
        :param opinion: an opinion (a word)
        :return: bool
        """
        opinions = eval(dict_string)[aspect].lower().split()
        return True if opinion.lower() in opinions else False

    def _is_be(self, x: int, sentence_blob: TextBlob) -> bool:
        """
        Check whether the word (sentence_blob[x]) is one of ['am','is','are','was','were']

        :param x: the index (x-th item in sentence_blob)
        :param sentence_blob: a TextBlob object
        :return: bool
        """
        return True if self._valid(x, sentence_blob) and sentence_blob.words[x].lower() in ['am', 'is', 'are', 'was',
                                                                                           'were'] else False

    def _add_word(self,
                  index: int,
                  word_list: list,
                  sentence_blob: TextBlob) -> list:
        """
        Extract the adverb or adjective;
        Judge whether the index-th word in sentence_blob is an adverb or adjective;
        The word "very" or "really" is not counted

        :param index: the index (x-th item in word_list)
        :param word_list: a list of words
        :param sentence_blob: a TextBlob object
        :return: the enriched word list
        """
        if self._valid(index, sentence_blob):
            if sentence_blob.tags[index][1] in ['RB', 'RBR', 'RBS', 'JJ', 'JJR', 'JJS'] and \
                    sentence_blob.tags[index][0].lower() not in ['very', 'really']:
                word_list.append(sentence_blob.tags[index][0].lower().strip())
        return word_list

    def _extract_attributes_pref(self,
                                 first_word_index: int,
                                 sentence_blob: TextBlob) -> str:
        """
        Extract the attributes that are right before the aspect in the sentence;
        We look at no more than 2 words before;
        Only when there's a adj/adv one index before the aspect will we look at the work 2 indexes before;

        e.g. "delicious warm coffee" --> {'coffee': 'warm delicious'}
             "weather was perfect. The coffee ..." --> {'coffee': ''}
             "Very friendly staff" --> {'staff': 'friendly'}

        :param first_word_index: the index of the first word in the aspect in the sentence
        :param sentence_blob: the sentence blob where the aspect locates
        :return: the attributes of the aspect in a string (words are separated by ' ')
        """
        pref_words = []

        pref_words = self._add_word(first_word_index - 1, pref_words, sentence_blob)

        # only when there's a adj/adv one index before the aspect will we look at the work 2 indexes before
        if len(pref_words) > 0:
            self._add_word(first_word_index - 2, pref_words, sentence_blob)

        return ' '.join(pref_words)

    def _extract_attributes_suff(self,
                                 ca_last_index: int,
                                 sentence_blob: TextBlob) -> str:
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
        :return: the attributes of the aspect in a string (words are separated by ' ')
        """
        suff_words = []

        # the adj/adv must come after the "be noun"
        if self._is_be(ca_last_index + 1, sentence_blob):
            suff_words = self._add_word(ca_last_index + 2, suff_words, sentence_blob)

        # only when there's a qualified adj/adv 2 index after the aspect will we look at the word 3 indexes after
        if len(suff_words) > 0:
            suff_words = self._add_word(ca_last_index + 3, suff_words, sentence_blob)

        # or if the word after 'be' is very or really, we will look at the word 3 indexes after
        if sentence_blob.tags[ca_last_index + 2][0].lower() in ['very', 'really']:
            suff_words = self._add_word(ca_last_index + 3, suff_words, sentence_blob)

        attr = ' '.join(suff_words)
        if len(suff_words) == 2 and suff_words[0] in ['not', "n't"]:
            attr = ''.join(suff_words)

        return attr

    def _opinion_extractor(self,
                           candidate_aspects: list,
                           sentence_blob: TextBlob) -> dict:
        """
        Extract the aspects and opinions associated with them in a sentence; returns a dictionary

        :param candidate_aspects: a list of aspects for extracting their opinions
        :param sentence_blob: the TextBlob object of the sentence that we are analyzing
        :return: a dictionary with the aspects as keys and the opinions wrapped up as a single string of words
                 separated with ' ' e.g. {'bedroom': 'sunny spacious', 'wardrobe': 'beautiful'}
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
                    aspect_opinion_dict[a] = self._extract_attributes_pref(first_word_index, sentence_blob)
                    # extract the attributes that appear after the aspect in the sentence
                    aspect_opinion_dict[a] = ' '.join(
                        [aspect_opinion_dict[a], self._extract_attributes_suff(last_word_index, sentence_blob)])
                except:
                    pass

        return aspect_opinion_dict

    def _aspect_opinion_for_one_sentence(self, sentence: str) -> dict:
        """
        Extract aspects and opinions for one sentence

        :param sentence: the sentence for analyzing
        :return: a dictionary with the aspects as keys and the opinions wrapped up as a single string of words
                 separated with ' ' e.g. {'bedroom': 'sunny spacious', 'wardrobe': 'beautiful'}
        """
        sentence = str(sentence).lower()
        sentence_blob = TextBlob(sentence)
        candidate_aspects = self.aspect_extractor(sentence)
        aspect_opinion_dict = self._opinion_extractor(candidate_aspects, sentence_blob)

        return aspect_opinion_dict

    def aspect_opinion_for_one_comment(self, comment: str) -> dict:
        """
        Extract aspects and opinions for one comment (which can consist of many sentences)

        :param comment: the comment for analyzing
        :return: a dictionary with the aspects as keys and the opinions wrapped up as a single string of words
                 separated with ' ' e.g. {'bedroom': 'sunny spacious', 'wardrobe': 'beautiful'}
        """
        sentences = sent_tokenize(comment)

        aspect_opinion_dict = {}
        for sentence in sentences:
            aspect_opinion_dict = self._merge_two_dicts(
                aspect_opinion_dict,
                self._aspect_opinion_for_one_sentence(sentence))
        return aspect_opinion_dict

    def aspect_opinon_for_all_comments(self, report_interval: int = None):
        """
        Extract aspects and opinions for all the comments in a pandas dataframe;

        :param report_interval: the function will report progress every `report_interval` rows
        :return: a pandas dataframe with id, reviews and the string version of the aspect_opinion_dict
        """
        df = self.df[self.df[self.review_column].notna()].copy()
        df = df.reset_index().drop('index', axis=1)
        id_column = self.id_column
        review_column = self.review_column

        begin = datetime.datetime.now()
        print("Aspect Opinion Extractor job begins: {}".format(begin))
        aspect_opinion_dict_all = {}  # a dictionary for all the aspects and opinions in the reviews data
        df_small = df[[id_column, review_column]].copy()
        df_small['aspects_opinions'] = ""  # add a new column for aspects and opinions in the comment

        if report_interval is not None:
            report_interval = report_interval
        elif len(df) > 500:
            report_interval = int(len(df) / 10)
        else:
            report_interval = len(df)

        print("There are in total {} comments. We will report progress every {} comments."\
              .format(len(df), report_interval))

        for i in range(len(df)):
            d = self.aspect_opinion_for_one_comment(df_small.loc[i, review_column])
            aspect_opinion_dict_all = self._merge_two_dicts(aspect_opinion_dict_all, d)
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
        aspects_opinions_df = aspects_opinions_df[aspects_opinions_df['opinions'] != ""] \
            .sort_values(by=['pop'],
                         ascending=False).drop('pop', 1)

        self.df_with_aspects_opinions = df_small
        self.aspects_opinions_df = aspects_opinions_df

    def most_popular_opinions(self, aspect: str, num_top_words: int = 10) -> pd.DataFrame:
        """
        Collect the most popular opinion words for an aspect

        :param aspect: aspect (in a string)
        :param num_top_words: numbers of most common opinions
        :return: a dataframe with the most popular opinion words associated with the aspect
        """
        ao_df = self.aspects_opinions_df.copy()
        df = self.df_with_aspects_opinions.copy()
        # choose the most popular opinions of the aspect
        opinion_top_words = pd.Series(ao_df.set_index("aspects").loc[aspect, 'opinions'].split()) \
                                .value_counts()[:num_top_words].index.tolist()
        # a subset of the comments that have the aspect
        comments_contain_aspect = df[df['aspects_opinions'].apply(self._has_aspect, aspect=aspect)]
        perc = []  # percentage of the comments with the aspects having that opinion

        # count the frequences of the opinions
        for o in opinion_top_words:
            comments_contain_aspect_and_opinion = comments_contain_aspect[
                comments_contain_aspect['aspects_opinions'].apply(self._has_opinion, aspect=aspect, opinion=o)]
            perc.append(round(len(comments_contain_aspect_and_opinion) / len(comments_contain_aspect), 2) * 100)

        aspect_plot = pd.DataFrame({'opinion': opinion_top_words, "% of people use this word": perc}) \
            .sort_values(['% of people use this word', 'opinion'], ascending=False)
        return aspect_plot

    def single_aspect_view(self, aspect: str,
                           num_top_words: int = 10,
                           change_figsize: bool = True,
                           xticks_rotation: int = 45,
                           _testing = False):
        """
        plot popular opinions around an aspect;
        For example, we are interested in what people say about "staff",
        We pick the top n popular words people used to describe staff and calculalte among those who have expressed
        opinion towards "staff", how many percentage of them used certain words;
        The output will be a bar chart that shows the most popular opinion words associated with the aspect, and
        their proportions

        :param aspect: aspect (in a string)
        :param num_top_words: numbers of most common opinions
        :param change_figsize: bool; change the figsize or not
        :param xticks_rotation: rotation degree of the xticks
        :param _testing: bool; If True, the function won't show the chart

        :return: a bar chart
        """
        style.use('fivethirtyeight')

        aspect_plot = self.most_popular_opinions(aspect, num_top_words)

        if change_figsize:
            plt.rcParams['figure.figsize'] = (num_top_words, 5)
        plt.xticks(rotation=xticks_rotation)
        plt.rcParams['xtick.labelsize'] = 20.0

        df = self.df_with_aspects_opinions.copy()
        comments_contain_aspect = df[df['aspects_opinions'].apply(self._has_aspect, aspect=aspect)]

        ax = sns.barplot(x='opinion', y="% of people use this word", data=aspect_plot)
        ax.set_title("What do people say about {} ? (total {} mentions)".format(aspect, len(comments_contain_aspect)))
        ax.set(xlabel="")

        if not _testing:
            plt.show()

        return ax

    def popular_aspects_view(self, _testing=False):
        """
        Quick plot: single_aspect_view for the top 9 aspects
        """
        style.use('fivethirtyeight')
        plt.rcParams.update({'font.size': 10})
        plt.rcParams['figure.figsize'] = (15, 15)
        plt.rcParams['xtick.labelsize'] = 10.0
        plt.rcParams['ytick.labelsize'] = 10.0

        df = self.df_with_aspects_opinions.copy()
        self.top_aspects = self.aspects_opinions_df.aspects \
                               [~self.aspects_opinions_df['aspects'].isin(self.aspect_mute_list)][:9].values

        fig, axes = plt.subplots(3, 3)
        x = [0, 0, 0, 1, 1, 1, 2, 2, 2]
        y = [0, 1, 2, 0, 1, 2, 0, 1, 2]

        for i in range(9):
            aspect_plot = self.most_popular_opinions(self.top_aspects[i], 10)
            comments_contain_aspect = df[df['aspects_opinions'].apply(self._has_aspect, aspect=self.top_aspects[i])]

            sns.barplot(x='opinion',
                        y="% of people use this word",
                        data=aspect_plot,
                        ax=axes[x[i], y[i]])
            axes[x[i], y[i]].set_title(
                "What do people say about {} ? (total {} mentions)" \
                    .format(self.top_aspects[i], len(comments_contain_aspect)),
                fontsize=12
            )
            axes[x[i], y[i]].set(xlabel="")
            axes[x[i], y[i]].tick_params(axis='x', rotation=45)
            plt.xticks(rotation=45)

        plt.subplots_adjust(hspace=0.5)
        plt.subplots_adjust(wspace=0.5)

        if not _testing:
            plt.show()
