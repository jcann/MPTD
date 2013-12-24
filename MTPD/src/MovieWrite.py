# Filename:       MovieWrite.py
# Project:        MTPD
# Description:    MovieWrite class provides basic process for information
#                 writing for all movies
#
# Author:         Jonathan Cann

# History
# 2013-11-03 JC File creation
# 2013-12-23 JC Updated MovieWrite class to write movie details to CSV or SQL 
#               files. SQL file is formatted to insert statements. CSV file is
#               delimited for spreadsheet import. 

from MovieList import MovieList
from MovieSearch import MovieSearch
from Movie import Movie

import os

# Constants
EXT_SQL = ".sql"
EXT_CSV = ".csv"
SQL_MOVIE = "Movie"
SQL_GENRE = "Genre"
SQL_CAST  = "Cast"

class MovieWrite:
    
    # Constructor
    def __init__(self, file_path, file_name, movieList):
        self.file_path = file_path
        self.file_name = file_name
        self.movieList = movieList
        
    # Write inserts to SQL file
    def writeSql(self):
        file_name = self.file_name + EXT_SQL
        f_path = os.path.join(self.file_path, file_name)
        fd = open(f_path, "w")
        
        movieList = self.movieList.getMovieList()
        
        for movie in movieList:        
            query = "INSERT INTO %s VALUES (\"%s\", \"%s\", \"%s\")\n" % (SQL_MOVIE, movie.getId(), movie.getTitle(), movie.getReleaseDate())
            fd.write(query)
            
            query = "INSERT INTO %s VALUES (\"%s\", " % (SQL_GENRE, movie.getId()) 
            genre = movie.getGenre()
            for i in genre:
                query += "\"" + i + "\", "
            query = query.rstrip(", ") + ")\n"
            fd.write(query)

            query = "INSERT INTO %s VALUES (\"%s\", " % (SQL_CAST, movie.getId())            
            cast = movie.getCast()
            for j in cast:
                query += "\"" + j + "\", "
            query = query.rstrip(", ") + ")\n"
            fd.write(query)
        
        fd.close()
       
    # Write delimited data to CSV file
    def writeCsv(self):
        file_name = self.file_name + EXT_CSV
        f_path = os.path.join(self.file_path, file_name)

        data = self.movieList.getString()
        fd = open(f_path, "w")
        fd.write(data)
        fd.close()

if __name__=='__main__':
    API_KEY = "447ecf40bf72a3fa6218f3024465a567"
    
    movieNew = Movie()
    movieList = MovieList()
    movieSearch = MovieSearch(API_KEY)
    movieId = movieSearch.getId("Pi")
    movieNew = movieSearch.getDetails(movieId, "credits")
    movieList.setMovie(movieNew)    
    movieId = movieSearch.getId("1408")
    movieNew = movieSearch.getDetails(movieId, "credits")
    movieList.setMovie(movieNew)
    
    tempMovieWrite = MovieWrite("./", "temp", movieList)   
    tempMovieWrite.writeCsv()
    tempMovieWrite.writeSql()     