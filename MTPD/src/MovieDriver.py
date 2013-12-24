# Filename:       MovieDriver.py
# Project:        MTPD
# Description:    MovieDriver class provides basic driver to query and write
#                 movie title information
#
# Author:         Jonathan Cann

# History
# 2013-11-03 JC File creation
# 2013-12-23 JC Updated MovieDriver class to read, query, write movie titles.

from Movie import Movie
from MovieList import MovieList
from MovieSearch import MovieSearch
from MovieWrite import MovieWrite

import os

#Constants
SUCCESS =  "Success"
FAILURE = "Failure"

class MovieDriver:
    
    # Constructor
    def __init__(self, api_key):
        self.movieList = MovieList()
        self.movieSearch = MovieSearch(api_key)
        self.titles = []
        self.failed = []
    
    # Read movie titles from file
    def readFile(self, file_path):
        print "Reading movie titles from file..."
        fd = open(file_path, "r")
        
        for title in fd.readlines():
            self.titles.append(title.rstrip())
        
        fd.close()

    # Write movie details to file
    def writeFile(self):
        f_path = ""
        while not os.path.isdir(f_path):
            f_path = raw_input("ENTER FILE PATH: ")

        f_name = raw_input("ENTER FILE NAME: ")
        
        movieWrite = MovieWrite(f_path, f_name, self.movieList)
        movieWrite.writeCsv()
    
    # Search movie details
    def searchMovies(self, append = None):
        movieNew = Movie()
        
        for name in self.titles:
            prntTitle = (name.rstrip())[0:59]            
            print "Searching for %s..." % prntTitle
            movieId = self.movieSearch.getId(name)
            
            if movieId is not None:
                movieNew = self.movieSearch.getDetails(movieId, append)
                self.movieList.setMovie(movieNew)
            else:
                self.failed.append(name)
    
if __name__=='__main__':
    API_KEY = "447ecf40bf72a3fa6218f3024465a567"
    
    testMovieDriver = MovieDriver(API_KEY)
    testMovieDriver.readFile("C:/Users/cannj/Downloads/dev/01_FILMS.txt") 
    testMovieDriver.searchMovies("credits")
    testMovieDriver.writeFile()