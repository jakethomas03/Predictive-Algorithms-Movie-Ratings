# Predictive Algorithms for Movie Ratings

![Python badge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

1. [Description](#Description)
2. [Description of Data Set](#Description-of-Data-Set)
3. [Additional Documentation](#Additional-Documentation)


## Description 

Personalized recommendations have become a normal part of everyday life and it is easy to forget how complex these predictive algorithms truly are. In this project, I was able to begin learning the basics of algorithmic machine learning and gain an understanding about what goes into these increasingly common algorithms.

To begin this project, I used Python to read in a file of 100,000 user movie ratings, which we later used to algorithmically predict, test, filter, and experiment on this data. The ultimate goal of the project was to take a certain user within the data files provided, and present them with a movie recommendation based on their rating history as well as other users in the data set. The 6 data sets and their descriptions can be found in [Description of Data Set and Link](#Description-of-Data-Set). The project was split up into 3 phases, each with its own distinct purpose. 

The first phase's tasks were to read from the given files and store the information in appropriate data structures, to define a function that allows users to explore and understand the dataset, and to produce bar plots that visualize demographic diffrences in users' tastes for movies. The resulting bar plots can be found in *plots.pdf* in this repository. 

The second phase was for creating algorithms that will predict a given users rating for a movie they have not yet rated. We created 5 algorithms, each with different strategies. Descriptions of these algorithms can be found in *CS1210Project2 handout real.pdf; Phase 2*, in this repository. Next the prediction algorithms were evaluated using experiments that randomly partitioned the 100,000 ratings into a training set and a testing set. The 80,000 training set ratings were used to train the algorithms, and the 20,000 testing set ratings were ran through the algorithms and then compared to the actual ratings users had given to certain movies, resulting in an RMSE for each algorithm. This process was looped through 10 times, and I created a box and whisker plot to show the 10 RMSEs and how they compared to the actual rating. The box and whisker plot can be seen in *Phase2Plots.pdf* in this repository.

In the third phase, we were tasked with implementing a more complex rating prediction algorithm using the definition of similarity (found in *CS1210Project2 handout real.pdf; Phase 3*) and collaboratively filtering the ratings using a weighted average of ratings that a certain movie has received from users that are similar to the given user. These functions are extremely complicated and further explanation can be found in the handout. 

This project provided a really interesting insight into the basics of machine learning and the predictive algorithns that Netflix and other streaming platforms may use when they recommend movies to their customers.

## Description of Data Set

MovieLens data sets were collected by the GroupLens Research Project
at the University of Minnesota.
 
This data set consists of:
	* 100,000 ratings (1-5) from 943 users on 1682 movies. 
	* Each user has rated at least 20 movies. 
  * Simple demographic info for the users (age, gender, occupation, zip)

  * u.data
     -- The full u data set, 100000 ratings by 943 users on 1682 items. Each user has rated at least 20 movies.  Users and items arenumbered consecutively from 1.  The data is randomly ordered. This is a tab separated list of:
    | user id | item id | rating | timestamp 
     -- The time stamps are unix seconds since 1/1/1970 UTC
    
  * u.info
     -- The number of users, items, and ratings in the u data set.

  * u.item
     -- Information about the items (movies); this is a tab separated list of
         movie id | movie title | release date | video release date | IMDb URL | unknown
    
     -- The last 19 fields are the genres, a 1 indicates the movie is of that genre, a 0 indicates it is not; movies can be in several genres at once:
     | Action | Adventure | Animation | Children's | Comedy | Crime | Documentary | Drama | Fantasy | Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi | Thriller | War | Western |
             
     -- The movie ids are the ones used in the u.data data set.

   * u.genre    
     -- A list of the genres.

   * u.user    
    -- Demographic information about the users; this is a tab separated list of:
      | user id | age | gender | occupation | zip code

     -- The user ids are the ones used in the u.data data set.

  * u.occupation 

    -- A list of the occupations.



## Additional Documentation

Please read *CS1210Project2 handout real.pdf* for a significantly more in depth explanation of this project and the instructions for which it was based on. Credit to my professor Sriram Pemmaraju for creating this extremely interesting and engaging project. 
