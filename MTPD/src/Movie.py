# Filename:       Movie.py
# Project:        MTPD
# Description:    Movie class provides basic structure for information stored
#                 for each movie queried
#
# Author:         Jonathan Cann

# History
# 2013-11-03 JC File creation
# 2013-12-23 JC Updated Movie class to set and get movie details and poster 
#               path. Details are store in a dictionary using the names tmdbId,
#               title, releaseDate, genre, and cast for the associated values.
# 2013-23-24 JC Modified getString method to display movie details in a 
#               specific order.

DETAIL_KEYS = ['tmdbId', 'title', 'releaseDate', 'genre', 'cast']

class Movie:
    
    # Constructor
    def __init__(self, tmdbId = None, title = None, releaseDate = None,
                 genre = [], cast = [], posterPath = None):
        self.details = {}
        
        self.details['tmdbId'] = tmdbId
        self.details['title'] = title
        self.details['releaseDate'] = releaseDate
        self.details['genre'] = genre
        self.details['cast'] = cast
        
        self.posterPath = posterPath

    # Set tmdb id
    def setId(self, tmdbId):
        self.details['tmdbId'] = tmdbId
    
    # Set movie title
    def setTitle(self, title):
        self.details['title'] = title

    # Set movie release date
    def setReleaseDate(self, releaseDate):
        self.details['releaseDate'] = releaseDate
        
    # Set movie genre
    def setGenre(self, genre):
        self.details['genre'] = genre
        
    # Set movie cast
    def setCast(self, cast):
        self.details['cast'] = cast
    
    # Set movie poster path
    def setPosterPath(self, posterPath):
        self.posterPath = posterPath

    # Get tmdb id
    def getId(self):
        return self.details['tmdbId']
        
    # Get movie title
    def getTitle(self):
        return self.details['title']

    # Get movie release date
    def getReleaseDate(self):
        return self.details['releaseDate']
    
    # Get movie genre
    def getGenre(self):
        return self.details['genre']
        
    # Get movie cast
    def getCast(self):
        return self.details['cast']
    
    # Get movie poster path
    def getPosterPath(self):
        return self.posterPath
    
    def getDetails(self):        
        return self.details
    
    def getString(self, delim):
        movieString = ""
            
        for key in DETAIL_KEYS:
            if isinstance(self.details[key], list):
                tmp = self.details[key]
                for x in tmp:
                    movieString += x + delim
            else:
                movieString += self.details[key] + delim
        
        return movieString.rstrip(delim)
    
if __name__=='__main__':
    
    # Test Default Constructor
    tempMovie = Movie()
    tempMovie.setId("550")
    tempMovie.setTitle("Fight Club")
    tempMovie.setReleaseDate("1999-10-15")
    tempMovie.setGenre(['Action', 'Drama', 'Thriller'])
    tempMovie.setCast(['Edward Norton', 'Brad Pitt'])
    tempMovie.setPosterPath("/2lECpi35Hnbpa4y46JX0aY3AWTy.jpg")
    
    print "*** TEST ***"                  
    print tempMovie.getTitle()
    print tempMovie.getReleaseDate()
    print tempMovie.getGenre()
    print tempMovie.getCast()
    print tempMovie.getPosterPath()
    print tempMovie.getDetails()
    print tempMovie.getString(';')
    
    # Test Constructor
    tempMovie = Movie("550", "Fight Club", "1999-10-15", 
                      ['Action', 'Drama', 'Thriller'], 
                      ['Edward Norton', 'Brad Pitt'],
                      "/2lECpi35Hnbpa4y46JX0aY3AWTy.jpg")
    
    print "\n*** TEST ***"
    print tempMovie.getTitle()
    print tempMovie.getReleaseDate()
    print tempMovie.getGenre()
    print tempMovie.getCast()
    print tempMovie.getPosterPath()
    print tempMovie.getDetails()
    print tempMovie.getString(';')