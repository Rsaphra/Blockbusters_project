# Blockbusters

## Goal:
Gain insight into current trends in the movie making industry.  

## Data Sources:
__TMDb__:  The majority of data collection has revovled around The Movie Database site. Using TMDb we gathered a list of the top 1000 movies ever created.

__OMDb__: Supplemental data has been acquired from the Open Movies DB for the 1000 titles that were extracted from TMDb.

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

In order to complete our goal we utilized [Amazon Web Services](https://aws.amazon.com/ "Amazon Web Services") (AWS RDS) and initiated a database  instance to store all the data we gathered. To increase collaboration efficiency we used [GitHub](https://github.com/ "GitHub"); this allowed us to work uninterrupted, simultaneously, and independently.

The majority of our code was written in Jupyter Notebooks using Python. Furthermore, we used [VSCode](https://code.visualstudio.com/ "VSCode") to create 4 Python modules that contain all the functions we created. Additionaly, we used MySQL queries to interact with our AWS-RDS.

# Methodology

## Define Success

Definition: "the attainment of popularity or profit".

We defined success by focusing mainly on popularity. Followed by raising questions such as:

1. Are some genres more popular than others?
2. Which directors create the most popular movies?
3. Which movie genre creates the most revenue?

## Workflow

* Create AWS RDS Instance
* Create [DB Schema](#DB-Schema)
* Populate Tables
  * Gather data using [OMDb's](http://www.omdbapi.com/ "OMDb") and [TMDb's](https://www.themoviedb.org/?language=en-US "TMDb") own APIs
  * Clean data using Python to extract only what we might need.
* Data Analyses
  * Extract the relevant data using MySQL queries
  * Create visuals using [Matplotlib](https://matplotlib.org/ "Matplotlib")
  * Reach meaningful [conclusions](#Take-Home-Message)
  
## Results

We started out by looking at the distribution of genres within the top rated movies in TMDb. Out of the 1000 highest rated movies 28.8% of movies were tagged as "Dramas".

![Total Movies Per Genre Pie](Images/genre_pie.JPG "Total Movies Per Genre Pie")

Before we dove deeper into more analyses we first tested the two different rating metrics that were available to us (rotten tomatoes rating and TMDB's popularity) with the box office revenues to check which metric correlated better.

<img src=Images/rev_over_popu.JPG alt="[Popularity and Revenues" width="450"/> <img src=Images/rev_over_rating.JPG alt="RT Rating and Revenues" width="450"/>

Popularity correlated better with the average revenues (r=0.7349) than rotten tomatoes rating (r=0.0666). We followed by checking each genre's popularity.

<img src=Images/genre_popu.JPG alt="Revenue per genre chart" width="450"/>

Out of the 18 different tags drama movies were rated the 16th most popular. We continued by looking at the most popular drama movies comparing them to the most popular movies to check whether drama movies are not as good as the most popular ones (subjectively speaking).

<img src=Images/genre_pop_list.JPG alt="Most popular Dramas list" width="450"/>

<img src=Images/top10_pop_list.JPG alt="Most popular movies list" width="450"/>

Subjectively speaking the quality of dramatic cinema does not fall short in comparison to the most popular movies.

Our next step was to check the average revenue for each genre, top 12 directors, and to list the movies that made the most amount of money at the box office to see if there's a common  denominator.

<img src=Images/genre_revu.JPG alt="Revenue per Genre Bar Char" width="450"/>

<img src=Images/top_rev_direct.JPG alt="Revenue for Top 12 Directors Bar Char" width="450"/>

<img src=Images/top_rev_list.JPG alt="Highest Grossing Films List" width="450"/>

In addition to dramas not being most popular they also did not bring in the most amount of money at the box office.  However, we were able to find a possible common denominator between the highest grossing films.

## Take Home Message

This was just an initial scope. Our recommendation is focused more on what content not to create, dramatic cinema. The market is saturated and these movies and those movies are not the most so popular among viewers.

If an immediate decision has to be made, we would recommend filming an action/adventure movie, based on a comic series or book.

#### DB-Schema

<img src=Images/db_schema.JPG alt="DB Schema" width="450"/>

