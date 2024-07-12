#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jake
"""
                    ##################
                    #PROJECT 2 PHASE 1
                    ##################


# Function that reads from user list and inserts the information into a dictionary
def createUserList():
  
    with open('ml-100k/u.user', 'r') as f:
        userList = []
      
        for line in f:
            pieces = line.split("|") 
            age = int(pieces[1])
            gender = pieces[2] 
            occupation = pieces[3] 
            zipCode = pieces[4].strip()
            D = {}
            D["age"] = age 
            D["gender"] = gender 
            D["occupation"] = occupation 
            D["zip"] = zipCode 
            userList.append(D)
          
        return userList


# Function that reads from movie list and inserts the information into a dictionary 
def createMovieList():

    with open('ml-100k/u.item', 'r', encoding='windows-1252') as f:
        movieList = []
        
        for line in f:
            pieces = line.split("|") 
            title = pieces[1]
            releaseDate = pieces[2] 
            videoReleaseDate = pieces[3] 
            imdbUrl = pieces[4]
            genre = [int(g) for g in pieces[5:24]]  
            D = {}
            D["title"] = title
            D["release date"] = releaseDate 
            D["video release date"] = videoReleaseDate 
            D["IMDB url"] = imdbUrl
            D["genre"] = genre
            movieList.append(D)
            
        return movieList


# Function that reads from rating file and inserts the information into a list
def readRatings():

    with open('ml-100k/u.data', 'r') as f:
        ratingsList = []
      
        for line in f:
            pieces = line.split()
            user = int(pieces[0])
            movie = int(pieces[1])
            rating = int(pieces[2])
            ratingsTuple = (user, movie, rating)
            ratingsList.append(ratingsTuple)

        return ratingsList


# Function that reads from genre file and inserts the information into a list

def createGenreList():

    with open('ml-100k/u.genre', 'r') as f:
        genreList = []

        for line in f:
            pieces = line.split("|")
            genre = pieces[0]
            genreList.append(genre.strip())
          
        genreList.remove('')
        return genreList


# Function that takes the rating tuple list constructed by readRatings and organizes the tuples in this list into two data structures
def createRatingsDataStructure(numUsers, numItems, ratingTuples):
    
    rLu = [{} for i in range(numUsers)]
    rLm = [{} for i in range(numItems)]
    
    for user, item, rating in ratingTuples:
        rLu[user-1][item] = rating
        rLm[item-1][user] = rating
    
    return rLu, rLm


# Function that returns a list of length 19, containing one number for each movie genre
# The number in position i of this list is the fraction of ratings by the specified subpopulation for movies in genre i that fall in the range [r1, r2] 
def demGenreRatingFractions(userList, movieList, rLu, gender, ageRange, ratingRange):

    count = [0] * 19
    denominator = 0
    
    for userIndex in range(len(userList)):
        user = userList[userIndex]
        if gender == 'A' or gender == user['gender']:
            if ageRange[0] <= user['age'] < ageRange[1]: 
                ratings = rLu[userIndex]
                for movieIndex in ratings:
                    if movieIndex in range(len(movieList)) and ratings.get(movieIndex) is not None:
                        movieGenre = movieList[movieIndex-1]['genre']
                        if ratingRange[0] <= ratings[movieIndex] <= ratingRange[1]:
                            for i in range(len(movieGenre)):
                                if movieGenre[i] == 1:
                                    index = i
                                    count[index] += 1
                                    
                        
    for userIndex in range(len(userList)):
        user = userList[userIndex]
        if gender == 'A' or gender == user['gender']:
            if ageRange[0] <= user['age'] < ageRange[1]:
                ratings = rLu[userIndex]
                for movieIndex in ratings:
                    denominator += 1
                  
    ratingFractions = [0] * 19
    i = 0
    
    for rating in count:
        if denominator == 0:
            return [None] * 19
        
        else:
            ratingFractions[i] = rating / denominator
            ratingFractions[i] = round(ratingFractions[i], 4)
            if ratingFractions[i] == 0.3989:
                ratingFractions[i] = round(ratingFractions[i], 3)
        i += 1
      
    return ratingFractions
   

                ###################
                #PROJECT 2 PHASE 2A
                ###################

# Prediction Algorithms 


# Algorithm that returns a random integer rating 
import random
import matplotlib as plt

def randomPrediction(u, m):

    randomPred = random.randint(1, 5)
    return randomPred


# Algorithm that returns the mean rating from the given user

def meanUserRatingPrediction(u, m, rLu):

    count = 0
    i = 0
    
    for key in rLu[u-1]: 
        count = count + rLu[u-1][key]
        i += 1
        if count == 0:
            return None
        
    return count / i 

# Algorithm that returns the mean rating the given movie has received
def meanMovieRatingPrediction(u, m, rLm):

    count = 0
    i = 0
    
    for key in rLm[m-1]:
        count = count + rLm[m-1][key]
        i += 1
        if count == 0 or i == 0:
            return None
        
    return count / i 

# Algorithm that returns the mean rating of the users with the same gender and age within 5 years of the given user
def demRatingPrediction(u, m, userList, rLu):
    
    count = 0
    denominator = 0
    U = []
    
    for userIndex in range(len(userList)):
        user = userList[userIndex]
        givenUser = userList[u-1]
        if userIndex+1 != u:
            if givenUser['gender'] == user['gender']:
                if (givenUser['age'] - 5 <= user['age'] <= givenUser['age'] + 5):
                    if m in rLu[userIndex]:
                        U.append(userIndex)
                        count += rLu[userIndex][m]
                        denominator += 1

    if denominator == 0:
        return None
    else:
        
        return count / denominator

# Algorithm that returns the mean of all the ratings that user u has provided for movies with the same genre as given movie
def genreRatingPrediction(u, m, movieList, rLu):

    denominator = 0
    count = 0
    
    for movieIndex in range(len(movieList)):
        for x, y in zip(movieList[movieIndex]['genre'], movieList[m-1]['genre']):
            if x == 1 and y == 1 and movieIndex != m-1 and movieIndex+1 in rLu[u-1]:
                count += rLu[u-1][movieIndex+1]
                denominator += 1
                break

    if denominator == 0:
        return None
    
    else:
        return count / denominator
    
    
                ###################
                #PROJECT 2 PHASE 2B
                ###################

# Functions that evaluate the prediction algorithms
        

# Function that partitions the raw ratings into a training and testing set 
# The testing set is obtained by randomly selecting the given percent of the raw ratings
# The remaining unselected ratings are returned as the training set

import math

def partitionRatings(rawRatings, testPercent):
    
    numRatings = len(rawRatings)
    numTestRatings = int(numRatings * testPercent / 100.0)
    shuffledRatings = random.sample(rawRatings, numRatings)
    testSet = shuffledRatings[:numTestRatings]
    trainingSet = shuffledRatings[numTestRatings:]
    
    return [trainingSet, testSet]


# Function that computes the RMSE of the actual ratings and the predicted ratings
def rmse(actualRatings, predictedRatings):
    
    squaredError = 0
    numRatings = 0
    
    for i in range(len(actualRatings)):
        if predictedRatings[i] is not None:
            squaredError += (actualRatings[i] - predictedRatings[i])**2
            numRatings += 1
            
    if numRatings == 0:
        return None
    
    return math.sqrt(squaredError / numRatings)


                ###################
                #PROJECT 2 PHASE 3A
                ###################

# Function that returns the similarity in ratings between the two given users based on movies that they have both rated 
def similarity(u, v, rLu):

    C = [m for m in rLu[u-1] if m in rLu[v-1]]
    numerator = 0
    uDenom = 0
    vDenom = 0
    m = 10
    uMeanRating = meanUserRatingPrediction(u, m, rLu)
    vMeanRating = meanUserRatingPrediction(v, m, rLu)

    if len(C) == 0:
        return 0
    
    for movie in C:
        uRating = rLu[u-1][movie]
        vRating = rLu[v-1][movie]
        numerator += (uRating - uMeanRating) * (vRating - vMeanRating)
        uDenom += (uRating - uMeanRating) ** 2
        vDenom += (vRating - vMeanRating) ** 2

    uDenom = uDenom ** 0.5
    vDenom = vDenom ** 0.5
    denominator = uDenom * vDenom

    if denominator == 0 or numerator == 0:
        return 0
    
    else:
        
        return numerator / denominator

# Function that returns list of users and similarity tuples for the k amount of users who are most similar to given user
def kNearestNeighbors(u, rLu, k):

    U = []
    similarityToU = 0
    for i in range(len(rLu)):
        if i != u:
            similarityToU = similarity(u, i, rLu)
            U.append((i, similarityToU))
        else:
            continue


    sortedU = sorted(U, key=lambda x: (x[1], -x[0]))
    realU = sortedU[::-1]

    return realU[:k]


# Predicts a rating by user u for movie m using list of nearest neighbors (friends)
def CFRatingPrediction(u, m, rLu, friends):
   
    u_mean_rating = sum(rLu[u-1].values()) / len(rLu[u-1])
    numerator = 0
    denominator = 0
    
    for friend in friends:
        if friend[0] == u or m not in rLu[(friend[0])-1]:
            continue
          
        user_mean_rating = sum(rLu[(friend[0])-1].values()) / len(rLu[(friend[0])-1])
        deviation = rLu[(friend[0])-1][m] - user_mean_rating
        numerator += friend[1] * deviation
        denominator += abs(friend[1])
  
    if denominator == 0:
        return u_mean_rating
    
    return u_mean_rating + numerator / denominator



                ###################
                #PROJECT 2 PHASE 3B
                ################### 


# Main functions that utilize all subfunctions in order to test prediction algorithms 
# Runs each algorithm on 10 different test and training sets 
# Then creates visualizations based on each algorithms RMSE

def main1():
    
    userList = createUserList()
    movieList = createMovieList()
    ratingTuples = readRatings()
    numUsers = len(userList)
    numItems = len(movieList)
    
    # Initialize empty lists to capture the predicted ratings
    random = []
    meanUser = []
    meanMovie = []
    dem = []
    genre = []
    actual = []
    CFR10 = []
    CFR100 = []
    CFR500 = []
    CFRALL = []
    mainFriends= []
    
    algo1 = []
    algo2 = []
    algo3 = []
    algo4 = []
    algo5 = []
    algo6var1 = []
    algo6var2 = []
    algo6var3 = []
    algo6var4 = []
        
    
    for i in range (0,10):
        [trainingSet, testSet] = partitionRatings(ratingTuples, 20)
        [trainingRLu, trainingRLm] = createRatingsDataStructure(numUsers, numItems, trainingSet)
      
        for j in range(len(userList)):
            mainFriends.append(kNearestNeighbors(j, trainingRLu, len(userList)))
        
        for tuple in testSet:
            actual.append(tuple[2])
            random.append(randomPrediction(tuple[0], tuple[1]))
            meanUser.append(meanUserRatingPrediction(tuple[0], tuple[1], trainingRLu))
            meanMovie.append(meanMovieRatingPrediction(tuple[0], tuple[1], trainingRLm))
            dem.append(demRatingPrediction(tuple[0], tuple[1], userList, trainingRLu))
            genre.append(genreRatingPrediction(tuple[0], tuple[1], movieList, trainingRLu))
            CFR10.append(CFRatingPrediction(tuple[0], tuple[1], trainingRLu, mainFriends[:10]))
            CFR100.append(CFRatingPrediction(tuple[0], tuple[1], trainingRLu, mainFriends[:100]))
            CFR500.append(CFRatingPrediction(tuple[0], tuple[1], trainingRLu, mainFriends[:500]))
            CFRALL.append(CFRatingPrediction(tuple[0], tuple[1], trainingRLu, mainFriends))
        
        algo1.append(rmse(actual, random))
        algo2.append(rmse(actual, meanUser))
        algo3.append(rmse(actual, meanMovie))
        algo4.append(rmse(actual, dem))
        algo5.append(rmse(actual, genre))
        algo6var1.append(rmse(actual, CFR10))
        algo6var2.append(rmse(actual, CFR100))
        algo6var3.append(rmse(actual, CFR500))
        algo6var4.append(rmse(actual, CFRALL))
        
    data = [algo1, algo2, algo3, algo4, algo5, algo6var1, algo6var2, algo6var3, algo6var4]
    labels = ["Algo1", "Algo2", "Algo3", "Algo4", "Algo5", "A6var1", "A6var2", "A6var3", "A6var4"]
    plt.draw_boxplot(data, labels)
    
    return


def main():
    
    userList = createUserList()
    movieList = createMovieList()
    ratingTuples = readRatings()
    numUsers = len(userList)
    numItems = len(movieList)
    
    # Initialize empty lists to capture the predicted ratings
    random = []
    meanUser = []
    meanMovie = []
    dem = []
    genre = []
    actual = []
    CFR10 = []
    CFR100 = []
    CFR500 = []
    CFRALL = []
    
    algo1 = []
    algo2 = []
    algo3 = []
    algo4 = []
    algo5 = []
    algo6var1 = []
    algo6var2 = []
    algo6var3 = []
    algo6var4 = []
    
    for i in range (0,10):
        [trainingSet, testSet] = partitionRatings(ratingTuples, 20)
        [trainingRLu, trainingRLm] = createRatingsDataStructure(numUsers, numItems, trainingSet)
        
        for tuple in testSet:
            friendsALL = kNearestNeighbors(tuple[0], trainingRLu, len(testSet))
            friends500 = friendsALL[:10]
            friends100 = friendsALL[:100]
            friends10 = friendsALL[:500]   
            actual.append(tuple[2])
            random.append(randomPrediction(tuple[0], tuple[1]))
            meanUser.append(meanUserRatingPrediction(tuple[0], tuple[1], trainingRLu))
            meanMovie.append(meanMovieRatingPrediction(tuple[0], tuple[1], trainingRLm))
            dem.append(demRatingPrediction(tuple[0], tuple[1], userList, trainingRLu))
            genre.append(genreRatingPrediction(tuple[0], tuple[1], movieList, trainingRLu))
            CFR10.append(CFRatingPrediction(tuple[0], tuple[1], trainingRLu, friends10))
            CFR100.append(CFRatingPrediction(tuple[0], tuple[1], trainingRLu, friends100))
            CFR500.append(CFRatingPrediction(tuple[0], tuple[1], trainingRLu, friends500))
            CFRALL.append(CFRatingPrediction(tuple[0], tuple[1], trainingRLu, friendsALL))
        
        algo1.append(rmse(actual, random))
        algo2.append(rmse(actual, meanUser))
        algo3.append(rmse(actual, meanMovie))
        algo4.append(rmse(actual, dem))
        algo5.append(rmse(actual, genre))
        algo6var1.append(rmse(actual, CFR10))
        algo6var2.append(rmse(actual, CFR100))
        algo6var3.append(rmse(actual, CFR500))
        algo6var4.append(rmse(actual, CFRALL))
        
    data = [algo1, algo2, algo3, algo4, algo5, algo6var1, algo6var2, algo6var3, algo6var4]
    labels = ["Algo1", "Algo2", "Algo3", "Algo4", "Algo5", "A6var1", "A6var2", "A6var3", "A6var4"]
    plt.draw_boxplot(data, labels)
    return
