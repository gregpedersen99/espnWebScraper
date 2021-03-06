#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 10:47:40 2022

@author: gregpedersen
"""

#This is a program that will be built upon later, for now, I am going to build 
#it out as a web scraper for ESPn.

import requests
from bs4 import BeautifulSoup
import pandas as pd


#Class=ScorweCell__Score gives us the actual game scores 
#next need to find team names (nets, bucks, 76ers, bulls)


#Overall Code to run the program, it just takes the date input 
#(which is harcoded for now until its more functional) and runs functions
def run_program():
    date = int(input("Please enter the date (YYYY/MM/DD): "))
    myUrl = get_date("20220512")
    scores = display_page(myUrl)
    #for every game in the scores variable returned by display_page
    for element in scores:
        #set the gameID parameter 
        gameID = element['gameID']
        #pass through boxscore function to get bos score 
        boxScore = scrapeStats(gameID)
        #Print the team scores (subject to chage)
        print(element['Team1'], element['Team1_Score'])
        print(element['Team2'], element['Team2_Score'])
        #Print the box scores
        team1 = getTeamStats(boxScore[0])
        team2 = getTeamStats(boxScore[1])
        print(team1.iloc[:,0:12])
        print(team2.iloc[:,0:12])
    


#This function takes a dater argument and creates a URL to find the page of 
#the date
def get_date(date):
    new_date = str(date)
    schedule_date_url = "https://www.espn.com/nba/scoreboard/_/date/" + new_date
    return(schedule_date_url)


#This function takes a url argument and finds the page of that URL, scraping 
#the teams and the scores in the process. 

def display_page(url):
    #finds the page according to the url 
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    #Looked through the document and found that using the classes is probably
    #the best way to do this 
    days = soup.find_all(class_ = "ScoreCell__Score")
    names = soup.find_all(class_="ScoreCell__TeamName")
    IDs = soup.find_all(class_="AnchorLink Button Button--sm Button--anchorLink Button--alt mb4 w-100")
    #print(soup.prettify()) #Use this to see structure
    nameList = list()
    scoreList = list()
    IDList = list()
    gameDict = {}
    
    
    #this for loop takes the names and day classes we found above,
    #cleans up the strings, then stores them in lists to be used later. 
    #Ideally we would store this in a dictionary, but I think thats something
    #we could figure out later. 
      
    for ID in range(0, len(IDs)):
       dummyID = str(IDs[ID])
       numeric_filter = filter(str.isdigit, dummyID)
       numeric_string = "".join(numeric_filter)
       numeric_string2 = numeric_string[4:-1]
       IDList.append(numeric_string2)
       IDsList = list(dict.fromkeys(IDList))
   
       
       #ID2 = dummyID[dummyID.find('nba/game/_/gameId/')+1:]
       #print(ID2)
        #ID3 = ID2[:ID2.find('"tabindex')]
        #IDList.append(ID3)
        
    for day in range(0, len(days)):
        dummyScore = str(days[day])
        score2 = dummyScore[dummyScore.find('>')+1:]
        score = score2[:score2.find('<')]
        scoreList.append(score)
 
#This loop worked better split in two since they have different indexes
#there will always be names displayed, but not scores, since some of the 
#games haven't happened. 
    for day in range(0, len(names)):
        dummyname = str(names[day])
        name2 = dummyname[dummyname.find('>')+1:]
        name = name2[:name2.find('<')]
        nameList.append(name)

#This loop appens a 0 to the end of score lists to deal with discrepancies,
#we can use this placeholder to display the teams but no score since the games
#may not have happened yet 
        
    for i in range(0, len(nameList)-len(scoreList)):
        scoreList.append(0)
    
    gameScoresList = []
#Pretty big for loop here that creates the a list of dictionaries for each game
#although we dont need dictionaries to display the scores, this helps us keep the 
#data organized
    for i,k,j,l, m in zip(nameList[0::2], nameList[1::2], scoreList[0::2], scoreList[1::2], IDsList[0:len(IDsList)]):
        if str(j) == '0':
            gameDict['Team1']= str(i)
            gameDict['Team2'] = str(k)
            gameDict['Team1_Score'] = 'na'
            gameDict['Team2_Score'] = 'na'
            gameDict['gameID'] = str(m)


        else:
            gameDict['Team1']= str(i)
            gameDict['Team2'] = str(k)
            gameDict['Team1_Score'] = str(j)
            gameDict['Team2_Score'] = str(l)
            gameDict['gameID'] = str(m)
            
        gameScoresList.append(gameDict.copy())
            
        

                
    return(gameScoresList)
 

def scrapeStats(gameID):
    
    
#This chunk of code reads the page in by ID:
    schedule_date_url = 'https://www.espn.com/nba/boxscore/_/gameId/' + gameID
    page = requests.get(schedule_date_url)
    soup = BeautifulSoup(page.content, "html.parser")


#This chunk splits the page into table related infromation for team1 and team2(need better var names)
    team1 = str(soup.findAll('table')[1].findAll('tbody'))
    team2 = str(soup.findAll('table')[2].findAll('tbody'))
    return team1, team2


#This code splits the player stats from HTML up and creates lists for each pplayer
#This needs to become a dictionary, thats next step
import re


#This function scrapes game by game and pulls stats from ESPn, prints them out based around date input
#creates rosters, and displays stats to the end user. In addition, I also used this to calculate 
#gamescore, as its a good way to filter out the players we dont care as much about. For each game, each 
#roster is sorted by gamescore, and the players with the 3 highest scores are displayed for the end user.

def getTeamStats(team):
    df = pd.DataFrame(columns = ['name', 'position','minutes', 'fg', '3pt', 'ft', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', '+/-', 'pts'])

    updatelist = team.split('playercard') #using split to create a list after "playercard"
    for element in range(0, len(updatelist)): #taking the last observation off because it needs to be parsed separately
        trial = updatelist[element]
        players = []
        substring = "DNP" #Created these two strings so players that contain this are disqualified
        substring2 = "Has not"
        substring3 = "TEAM" #interesting issue fixed here. I originally didn't have this, but if theres no player that didn't play, this gives us an error. Good to know in the future going forward
#print(trial)
        trial2 = trial.split('class=') #split again on the class= strings 
        for element2 in trial2[1:]: #taking off the first element because its an unneeded naming parameter
            trial3 = str(re.search(">(.*)</", str(element2))) #Splitting between strings > and </
            trial4 = trial3[trial3.find('>')+1:] #These two lines fruther splits the strings among "<" and ">"
            trial5 = trial4[:trial4.find('<')]
            players.append(trial5) #Appends it to a list at the end, preferrably this would be a dictionary 
            #print(players)
        substring_in_list = any(substring in string for string in players) #return true if the string is found, false if not found 
        substring_in_list2 = any(substring2 in string for string in players)
        substring_in_list3 = any(substring3 in string for string in players)

        if substring_in_list == False: #If it containds the first string, check to see if it contains the second
            if substring_in_list2 == False: #If it contains the second string, disqualify it
                if substring_in_list3 == False: #If TEAM stats are part of it disqualify 
                    if len(players[:-1]) != 0: #Kinda lazy, but it was adding an empty list 
                        a_series = pd.Series(players[:-1], index = df.columns) #Create an series with new info
                        df = df.append(a_series, ignore_index=True) #Append series to the dataframe
    #now that we have all of our information, the next thing to do is calculate the gamescores 
    #Splitting the fg number into 2 for game score calculation
    newFg = df["fg"].str.split("-", n=1, expand = True)
    df["FGA"] = newFg[1]
    df["FGM"] = newFg[0]
    #Adding free throws for gamescore calculation 
    newFt = df["ft"].str.split("-", n=1, expand = True)
    df["FTA"] = newFt[1]
    df["FTM"] = newFt[0]
    
    df['pts'] = df["pts"].astype(str).astype(int)
    df['FGM'] = df["FGM"].astype(str).astype(int)
    df['OREB'] = df["OREB"].astype(str).astype(int)
    df['DREB'] = df["DREB"].astype(str).astype(int)
    df['STL'] = df["STL"].astype(str).astype(int)
    df['AST'] = df["AST"].astype(str).astype(int)
    df['BLK'] = df["BLK"].astype(str).astype(int)
    df['FGA'] = df["FGA"].astype(str).astype(int)
    df['FTM'] = df["FTM"].astype(str).astype(int)
    df['PF'] = df["PF"].astype(str).astype(int)
    df['TO'] = df["TO"].astype(str).astype(int)
    df['FTA'] = df["FTA"].astype(str).astype(int)

    df["FTMiss"] = df["FTA"] - df["FTM"]
    
    #now that we have set our typing, we need to use this to get our gamescore 
    #Game Score Formula=(Points)+0.4*(Field Goals Made)+0.7*(Offensive Rebounds)+0.3*(Defensive rebounds)+(Steals)+0.7*(Assists)+0.7*(Blocked Shots)- 0.7*(Field Goal Attempts)-0.4*(Free Throws Missed) ??? 0.4*(Personal Fouls)-(Turnovers)
    df["GS"]=df["pts"]+0.4*df["FGA"]+0.7*df["OREB"]+0.3*df["DREB"]+df["STL"]+0.7*df["AST"]+0.7*df["BLK"]-0.7*df["FGA"]-0.4*df["FTM"]-0.4*df["PF"]-df["TO"]
    
    df = df.sort_values('GS', ascending = False)
    df = df[0:3]
    
    df = df.iloc[:,[0,2,3,4,8,9,10,11,12,13,14,15,21]]
    #print(df)
    return(df)

#print(df)


run_program()    

#nexxt time, I want to add a better way to input the date, and put the time on display
#I then want to do the favorite players option, preferrably creating an algorithm for players that 
#are having really good games. Id also like to narrow down the box scores to exclude certain 
#stats, and show fewer players, preferrably, Id be able to sort by minutes and take the top couple? 
#not super sure how this feature is going to work. 
