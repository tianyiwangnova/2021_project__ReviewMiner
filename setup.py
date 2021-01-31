from setuptools import setup, find_packages

setup(name="reviewminer",
      version="1.0.0",
      description="Comprehensive text analysis on customers reviews data",
      author="Tianyi Wang",
      packages=find_packages(include=["reviewminer","reviewminer.core"]),
      author_email="tw2567@columbia.edu",
      install_requires=["pandas",
                        "textblob",
                        "nltk",
                        "datetime",
                        "seaborn",
                        "plotly",
                        "codecov",
                        "pytest",
                        "pytest-cov",
                        "pytest-mpl"
                        ]
      )
