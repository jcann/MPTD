# Filename:       MovieDriver.py
# Project:        MTPD
# Description:    MovieDriver class provides basic driver to query and write
#                 movie title information
#
# Author:         Jonathan Cann

# History
# 2013-11-03 JC File creation
# 2013-12-23 JC Updated MovieDriver class to read, query, write movie titles.
# 2013-12-25 JC Updated MovieDriver class to read input from keyboard. Added 
#               menu selection.

from Movie import Movie
from MovieList import MovieList
from MovieSearch import MovieSearch
from MovieWrite import MovieWrite

import os

#Constants
SUCCESS =  "Success"
FAILURE = "Failure"
OPTIONS = ['1', '2', '3', '4', '5', '6', '7', 'exit']

class MovieDriver:
    
    # Constructor
    def __init__(self, api_key):
        self.movieList = MovieList()
        self.movieSearch = MovieSearch(api_key)
        self.titles = []
        self.failed = []
    
    # Read movie titles from file
    def readFile(self):
        f_path = ""
        while not os.path.isdir(f_path):
            f_path = raw_input("ENTER FILE PATH: ")
            
        print "FILES"
        print "---------------------------"
        
        f_list = os.listdir(f_path)
        for f_name in f_list:
            print f_name

        f_name = ""
        while f_name not in f_list:
            f_name = raw_input("ENTER FILE NAME: ")
        
        print "READING MOVIES TITLES FROM FILE..."
        
        file_path = os.path.join(f_path, f_name)
        fd = open(file_path, "r")
        
        for title in fd.readlines():
            self.titles.append(title.rstrip())
        
        fd.close()
            
    # Read keyboard input
    def readInput(self):
        titleInput = ""

        print "INPUT MOVIE TITLES"        
        while True:
            titleInput = raw_input("(end to exit): ")
            
            if titleInput == 'end':
                break
            
            self.titles.append(titleInput.rstrip())
        
    # Print movie titles        
    def printTitles(self):
        print "MOVIE TITLES:"
        print "---------------------------"
        for title in self.titles:
            print title
        
    # Write movie details to file
    def writeFile(self, toWrite = 'csv'):
        f_path = ""
        while not os.path.isdir(f_path):
            f_path = raw_input("ENTER FILE PATH: ")

        f_name = raw_input("ENTER FILE NAME: ")
        
        movieWrite = MovieWrite(f_path, f_name, self.movieList)
        
        if toWrite == 'csv':
            movieWrite.writeCsv()
        else: 
            movieWrite.writeSql()
    
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
    movieDriver = MovieDriver(API_KEY)
    
    while True:
        print "MENU"
        print "---------------------------"    
        print "   1: FILE INPUT"
        print "   2: KEYBOARD INPUT"
        print "   3: PRINT TITLES"
        print "   4: SEARCH TITLES"
        print "   5: SEARCH TITLES W/ CAST"
        print "   6: WRITE CSV"
        print "   7: WRITE SQL"
        print "exit: EXIT"
        
        menuInput = ""
        while menuInput not in OPTIONS:
            menuInput = raw_input("SELECT AN OPTION: ")
        
        if menuInput == 'exit':
            break
        elif menuInput == '1':
            movieDriver.readFile()            
        elif menuInput == '2':
            movieDriver.readInput()
        elif menuInput == '3':
            movieDriver.printTitles()            
        elif menuInput == '4':
            movieDriver.searchMovies()
        elif menuInput == '5':
            movieDriver.searchMovies("credits")
        elif menuInput == '6':
            movieDriver.writeFile()            
        elif menuInput == '7':
            movieDriver.writeFile("sql")