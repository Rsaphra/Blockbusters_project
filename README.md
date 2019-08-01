# Blockbusters project</h1>

### Goal:
Analyze data about movie industry and glean meaningful conclussions to spear head a new project regarding video content 

### Data Sources:
__TMDb__: The majority of data collection has revovled around The Movie Database site. Using TMDb we gathered
a list of the top 200 movies ever created.

__OMDb__: Supplemental data has been acquired from OMDb for the 200 top rated movies by TMDb.

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

### Technical Description:

We began by defining what the company deems as success followed by raising the questions to help up conclude what creates a successful movie.
for example:

1. Are some genres more popular than others?

2. Are different genres more profitable than otheers

We then designed the db's pipeline and constructes it. 

We webscraped [OMDb](http://www.omdbapi.com/ "OMDb") and [TMDb](https://www.themoviedb.org/?language=en-US "TMDb") using their own APIs.
