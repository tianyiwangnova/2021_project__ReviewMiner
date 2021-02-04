import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name="reviewminer",
      version="1.0.0.2",
      description="Comprehensive text analysis on customers reviews data",
      author="Tianyi Wang",
      url="https://github.com/tianyiwangnova/2021_project__ReviewMiner",
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
                        ],
      long_description=README,
      long_description_content_type="text/markdown",
      classifiers=[
                "License :: OSI Approved :: MIT License",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.7",
            ],
      project_urls={
          'Documentation' : 'https://github.com/tianyiwangnova/2021_project__ReviewMiner/wiki/Documentation',
          'Source Code' : 'https://github.com/tianyiwangnova'
      }
      )
