# Blockbusters

## Goal:
Gain insight into current trends in the movie making industry.  

## Data Sources:
__TMDb__:  The majority of data collection has revovled around The Movie Database site. Using TMDb we gathered a list of the top 1000 movies ever created ([TMDb API](https://www.themoviedb.org/?language=en-US "TMDb")).

__OMDb__: Supplemental data has been acquired from the Open Movies DB for the 1000 titles that were extracted from TMDb ([OMDb API](http://www.omdbapi.com/ "OMDb")]).

| Data                   | Source |
| ---------------------- | ------ |
| Title                  | TMDb   |
| Realase Date           | TMDb   |
| Genre                  | TMDb   |
| Popularity             | TMDb   |
| Vote Count             | TMDb   |
| Vote Average           | TMDb   |
| Director               | OMDb   |
| Revenues               | OMDb   |
| Rotten Tomatoes Rating | OMDb   |

## Technical Description:

In order to complete our goal we utilized [Amazon Web Services](https://aws.amazon.com/ "Amazon Web Services") (AWS RDS) and initiated a databse  instance to store all the data we gather. To increase collaboration efficiency we used [GitHub](https://github.com/ "GitHub"), this allowed us to work uninterrupted, simultaneously, and independently.

The majority of our code was written in Jupyter Notebooks using Python. Furthermore, we used [VSCode](https://code.visualstudio.com/ "VSCode") (Python) to create 4 modules that contain all the functions we created. Additionaly, We used MySQL queries to interact with our AWS-RDS.

# Methodology

## Define Success

## Get Data

## Analyze Data

We began by defining what the company deems as success followed by raising the questions to help up conclude what creates a successful movie.
for example:

1. Are some genres more popular than others?

2. Are different genres more profitable than others

We then designed the db's pipeline and constructes it. 

We webscraped [OMDb](http://www.omdbapi.com/ "OMDb") and [TMDb](https://www.themoviedb.org/?language=en-US "TMDb") using their own APIs.
