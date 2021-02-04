from reviewminer.aspect_opinion import *
import plotly.express as px


class SentimentScore(AspectOpinionExtractor):
    """
    Sentiment related analysis on the reviews data
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
        AspectOpinionExtractor.__init__(self, df=df, id_column=id_column, review_column=review_column)

    @staticmethod
    def sentiment_for_one_comment(comment: str) -> float:
        """
        Calculalte sentiment score for one comment ==> the mean of (polarity * subjectivity) for each sentence
        (if the sentence has a non-zero polarity)

        :param comment: the comment (which can consist of multiple sentences)
        :return: a sentiment score
        """
        try:
            ctm_blob = TextBlob(comment)
            sentiment_scores = [s.sentiment.polarity * s.sentiment.subjectivity for s in ctm_blob.sentences if
                                s.sentiment.polarity != 0]
            result = sum(sentiment_scores) / len(sentiment_scores) if len(sentiment_scores) > 0 else 0
        except:
            result = 0
        return result

    @staticmethod
    def _return_negative_comments(comment: str) -> str:
        """
        Return all the sentences in a comment that have negative sentiment scores
        
        :param comment: the comment (which can consist of multiple sentences)
        :return: all negative sentences separated by ' '
        """
        try:
            ctm_blob = TextBlob(comment)
            negative_sentences = [str(s) for s in ctm_blob.sentences if s.sentiment.polarity < 0]
            if len(negative_sentences) > 0:
                return " ".join(negative_sentences)
        except:
            pass

    def overall_sentiment(self, _testing=False):
        """
        Plot the histogram of the sentiment scores for all the comments;
        """
        df = self.df.copy()

        sentiment_scores = df[self.review_column].apply(self.sentiment_for_one_comment)
        self.sentiment_scores_all = sentiment_scores
        print("Average sentiment score: {}".format(round(sentiment_scores.mean(), 2)))
        print("{}% of the comments are positive,； {}% of the comments are neutral; {}% of the comments are negative".
            format(
                round(100 * sum(sentiment_scores > 0) / len(sentiment_scores), 2),
                round(100 * sum(sentiment_scores == 0) / len(sentiment_scores), 2),
                round((100 * sum(sentiment_scores < 0) / len(sentiment_scores)), 2)
            )
        )
        plt.figure(figsize=(5, 5))
        plt.rc('xtick', labelsize=15)
        plt.rc('ytick', labelsize=15)

        fig, ax = plt.subplots()
        ax.hist(sentiment_scores)
        ax.set_title('Sentiment scores of all comments (avg: {})'.format(round(sentiment_scores.mean(), 2)),
                     fontsize = 20)

        if not _testing:
            plt.show()
        else:
            return fig

    def sentiment_for_one_aspect(self, aspect: str) -> float:
        """
        Return the average sentiment score for an aspect;
        Average sentiment score: the average of the sentiment scores of the opinion words

        :param aspect: the aspect for analyzing
        :return: the average of the sentiment scores of the opinion words
        """
        try:
            len(self.aspects_opinions_df)
        except AttributeError:
            self.aspect_opinon_for_all_comments()

        opinions = self.aspects_opinions_df.where(self.aspects_opinions_df.aspects == aspect).dropna() \
                   ['opinions'].values[0].split()

        opinions_polarities = [TextBlob(i).sentences[0].sentiment.polarity for i in opinions if
                               TextBlob(i).sentences[0].sentiment.polarity != 0]
        aspect_sent_score = sum(opinions_polarities) / len(opinions_polarities)
        return aspect_sent_score

    def aspects_radar_plot(self, aspects: list, _testing=False):
        """
        plot the sentiment score radar chart for designated aspects

        :param aspects: a list of aspects
        :return:
        """
        try:
            len(self.aspects_opinions_df)
        except AttributeError:
            self.aspect_opinon_for_all_comments()

        sentiment_scores = [self.sentiment_for_one_aspect(i) for i in aspects]

        aspects_sentiments = pd.DataFrame(dict(r=sentiment_scores, theta=aspects))
        fig = px.line_polar(aspects_sentiments,
                            r='r',
                            theta='theta',
                            line_close=True,
                            title='Sentiment scores of the most common aspects')

        if not _testing:
            fig.show()
        else:
            return 'plot finished'

    def return_all_negative_sentences(self) -> list:
        """
        Return all negative sentences in the reviews data

        :return:
        """
        df = self.df.copy()
        review_column = self.review_column

        negatives = list(df[review_column].apply(self._return_negative_comments).dropna())
        self.all_negative_sentences = negatives
        return negatives

    def negative_comments_by_aspects(self) -> dict:
        """
        :return: a dict ==> keys are the aspects; values are the sentences associated with the aspects
        """
        result = {}

        try:
            all_negative_comments = self.all_negative_sentences
        except AttributeError:
            all_negative_comments = self.return_all_negative_sentences()

        for n in all_negative_comments:
            aspects = self.aspect_extractor(n)
            for a in aspects:
                if a in result and n not in result[a]:
                    result[a].append(n)
                elif a not in result:
                    result[a] = [n]
        self.negative_comments_by_aspects_dict = result
        return result

    def negative_comments_view(self, _testing=False):
        """
        Barplot on the numbers of negative sentences of each aspect
        """
        try:
            count_df = self.negative_comments_by_aspects_dict.copy()
        except AttributeError:
            count_df = self.negative_comments_by_aspects().copy()

        for a in count_df:
            count_df[a] = len(count_df[a])
        count_df = pd.DataFrame(
            {'aspect': list(count_df.keys()), 'numbers_of_negative_sentences': list(count_df.values())}).sort_values(
            "numbers_of_negative_sentences", ascending=False)

        count_df = count_df[~count_df['aspect'].isin(self.aspect_mute_list)]

        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=20)
        plt.figure(figsize=(15, 5))
        plt.xticks(rotation=90)
        ax = sns.barplot(x='aspect', y="numbers_of_negative_sentences", data=count_df[:20])
        ax.set_title("Aspects with the most negative comments")

        if not _testing:
            plt.show()
        else:
            return ax

    def return_negative_comments_of_aspect(self, aspect: str) -> list:
        """
        Return all the negative comments related to an aspect in a list

        :param aspect: the aspect for analyzing
        :return: a list of all the related negative comments
        """
        try:
            negatives = self.negative_comments_by_aspects_dict.copy()
        except AttributeError:
            negatives = self.negative_comments_by_aspects().copy()

        if aspect in negatives:
            return negatives[aspect]
        else:
            print("There's no negative comments about '{}'".format(aspect))
            return list()
