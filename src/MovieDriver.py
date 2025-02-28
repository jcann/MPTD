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
# 2013-12-25 JC Added write of failed titles to file.
# 2014-01-19 JC Added search by ID and write result to display.
# 2014-01-25 JC Updated to process TV titles.

from Movie import Movie
from MovieList import MovieList
from MovieSearch import MovieSearch
from MovieWrite import MovieWrite

import os

#Constants
SUCCESS =  "Success"
FAILURE = "Failure"

MENU_OPTIONS = {
                '0' : 'FILE INPUT',
                '1' : 'KEYBOARD INPUT',
                '2' : 'PRINT TITLES',
                '3' : 'SEARCH ID',
                '4' : 'SEARCH ID W/ CAST',
                '5' : 'SEARCH TITLES',
                '6' : 'SEARCH TITLES W/ CAST',
                '7' : 'PRINT MOVIES',
                '8' : 'WRITE CSV',
                '9' : 'WRITE SQL',
                'quit' : 'QUIT'
                }

MEDIA_OPTIONS = {
                 'movie' : 'MOVIE',
                 'tv' : 'TV',
                 'quit' : 'QUIT'
                 }

EXT_FAIL = ".failed"

class MovieDriver:
    
    # Constructor
    def __init__(self, api_key, mediaType = "movie"):
        self.movieList = MovieList()
        self.movieSearch = MovieSearch(api_key, mediaType)
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
            
        if self.failed:   
            fail_name = f_name + EXT_FAIL
            fail_path = os.path.join(f_path, fail_name)
            fd = open(fail_path, "w")
            
            for title in self.failed:
                fd.write(title + "\n")
            
            fd.close()

    # Write movie details to display
    def writeDisplay(self):
        print "ID       TITLE                                                       RELEASE"
        print "-------- ----------------------------------------------------------- ----------"

        tempList = self.movieList.getMovieList()
        for k in tempList:                        
            print "%s %s %s" % (k.getId().rjust(8), (k.getTitle()[0:59].encode('ascii', 'replace')).ljust(59), k.getReleaseDate())
        
    # Search movie details by ID
    def searchId(self, append = None):
        movieNew = Movie()
        
        for movieId in self.titles:
            print "Retrieving for %s..." % movieId
            movieNew = self.movieSearch.getDetails(movieId, append)
            self.movieList.setMovie(movieNew)
    
    # Search movie details by title
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
            
    menuInput = ""
                
    while menuInput not in MEDIA_OPTIONS:
        menuInput = raw_input("SELECT MEDIA (quit to exit): ")

    if menuInput == 'quit':
        exit()
         
    movieDriver = MovieDriver(API_KEY, menuInput)
    
    while True:
        
        print "MENU"
        print "---------------------------"    
        for item in sorted(MENU_OPTIONS.keys()):
            print "%s: %s"%(str(item).rjust(4), MENU_OPTIONS[item])
                
        menuInput = ""
                    
        while menuInput not in MENU_OPTIONS:
            menuInput = raw_input("SELECT AN OPTION: ")
        
        if menuInput == 'quit':
            break
        elif menuInput == '0':
            movieDriver.readFile()            
        elif menuInput == '1':
            movieDriver.readInput()
        elif menuInput == '2':
            movieDriver.printTitles()            
        elif menuInput == '3':
            movieDriver.searchId()
        elif menuInput == '4':
            movieDriver.searchId("credits")
        elif menuInput == '5':
            movieDriver.searchMovies()
        elif menuInput == '6':
            movieDriver.searchMovies("credits")
        elif menuInput == '7':
            movieDriver.writeDisplay()
        elif menuInput == '8':
            movieDriver.writeFile()            
        elif menuInput == '9':
            movieDriver.writeFile("sql")