# Filename:       MovieList.py
# Project:        MTPD
# Description:    MovieList class provides basic structure for information
#                 stored for all movies queried
#
# Author:         Jonathan Cann

# History
# 2013-11-03 JC File creation
# 2013-12-23 JC Updated MovieList class to set and get movies to the list

from Movie import Movie

class MovieList:

    # Constructor
    def __init__(self):
        self.movieList = []
    
    # Set movie to the list
    def setMovie(self, movieNew):
        self.movieList.append(movieNew)
        
    # Get movie from the list by id
    def getMovie(self, movieId):
        for movie in self.movieList:
            if movie.getId() == movieId:
                return movie

        return None

    # Get movie list
    def getMovieList(self):
        return self.movieList
    
    # Get all movies from the list as a string
    def getString(self):
        movieString = ""
        for movieId in self.movieList:
            movieString += movieId.getString(';') + "\n"

        return movieString
    
if __name__=='__main__':
    tempMovieList = MovieList()
    
    for i in xrange(10):
        tempMovie = Movie(str(i), "Fight Club", "1999-10-15", 
                          ['Action', 'Drama', 'Thriller'], 
                          ['Edward Norton', 'Brad Pitt'],
                          "/2lECpi35Hnbpa4y46JX0aY3AWTy.jpg")

        tempMovieList.setMovie(tempMovie)
        
    print tempMovieList.getString()
    
    for j in xrange(10):
        tempMovie = tempMovieList.getMovie(str(j))
        
        if tempMovie is not None:
            print tempMovie.getString(';')
            
    print ""
            
    tempList = tempMovieList.getMovieList()
    for k in tempList:
        print k.getString(';')