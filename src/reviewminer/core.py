from textblob import TextBlob, WordList
import pandas as pd


class ColumnError(Exception):
    pass


class Reviews:
    """
    Information about the reviews data
    """

    def __init__(self,
                 df: pd.DataFrame = None,
                 id_column: str = None,
                 review_column: str = None):
        """
        Take a data frame where each row is a comment/review

        :param df: a data frame where each row is a comment/review; The data frame should have at least an ID column
                   that stores the unique IDs of the comments, and a review column where the actual comments/reviews
                   are stored; default: None
        :param id_column: the name of the column that stores the unique IDs of the comments; default: None
        :param review_column: the name of the column where the actual comments/reviews are stored; default: None
        """
        if df is not None:

            if id_column is not None:
                self._examine_id_column(df, id_column)
                self.id_column = id_column
            else:
                print("Haven't specified id_column (the name of the column that stores the unique IDs of the comments)")

            if review_column is not None:
                self._examine_review_column(df, id_column)
                self.review_column = review_column
            else:
                print("Haven't specified review_column (the name of the column where the actual comments/reviews are "
                      "stored)")

        else:
            print("There's no reviews data")

    @staticmethod
    def _examine_id_column(df, id_column):
        """
        Examine whether the column actually exists
        """
        if not isinstance(id_column, str):
            raise ColumnError("id_column should be a string")
        if id_column not in df.columns:
            raise ColumnError("id_column not in df.columns")

    @staticmethod
    def _examine_review_column(df, review_column):
        """
        Examine whether the column actually exists
        """
        if not isinstance(review_column, str):
            raise ColumnError("review_column should be a string")
        if review_column not in df.columns:
            raise ColumnError("review_column not in df.columns")


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
        sentence_blob = TextBlob(sentence)

        # extract noun phrases
        # e.g. "I love drinking orange juice" --> "orange juice"
        noun_phrases: WordList = sentence_blob.noun_phrases

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
