from reviewminer.sentiment import *


class ReviewMiner(SentimentScore):

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
        SentimentScore.__init__(self, df=df, id_column=id_column, review_column=review_column)

    def one_time_analysis(self, report_interval: int = None,_testing = False):
        """
        One time analysis to display popular aspects and opinions, distribution of sentiment scores of each comment,
        sentiment scores for common aspects, and aspects with the most negative comments

        :param aspect_mute_list: a list of potential aspects that you want to exclude from the analysis
        :param report_interval: When extracting all the aspects and opinions, the function will report progress
                                for every report_interval comments
        """

        try:
            self.df.shape
        except AttributeError:
            print("Please assign your review data to the class by `ReviewMiner.df = <your df>`, " \
                  "The table should be a pandas DataFrame. Please specify the id_column and review_" \
                  "column too")

        print("========= Popular aspects and opinions in the data =========")

        self.aspect_opinon_for_all_comments(report_interval = report_interval)
        self.popular_aspects_view(_testing=_testing)

        print("========= Sentiment Analysis =========")

        self.overall_sentiment(_testing=_testing)
        self.aspects_radar_plot(self.top_aspects, _testing=_testing)
        self.negative_comments_view(_testing=_testing)

        if _testing:
            return 1






