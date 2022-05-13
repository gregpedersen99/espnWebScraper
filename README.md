# espnWebScraper
This is an espn web scraping tool that I have in production

## App.py
This is the UI interface, theres still a ton of ground to make on this, I still need to link it to my backend code that runs the app

## Scraper.py
This is the backend code for this project. It essentially:
  -Take a date input
  -Returns the games and the scores for those games
  -Returns the stats for all players
  -Calculates the game score for each player, then sorts them by gamescore, read about GS here: https://itsxandery.com/do-stats-matter-in-basketball/
      -While Gamescore isn't perfect, it does all we need it to do, which is parse out the most relevant players, and leave the lesser known ones 
  -Returns the players with the best game score, so we can see only the most relevant numbers. 

