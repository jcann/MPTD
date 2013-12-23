# Filename:       MovieSearch.py
# Project:        MTPD
# Description:    MovieSearch class provides basic process for information
#                 queried for all movies
#
# Author:         Jonathan Cann

# History
# 2013-11-03 JC File creation
# 2013-12-23 JC Updated MovieSearch class to query themoviedb.org for IDs and 
#               details for movies. Details retained are id, title, release 
#               date, genres, cast, and poster path. Poster images are 
#               retrieved and returned to the caller.

from Movie import Movie

from urllib2 import Request, urlopen
from urllib import urlencode
from fuzzywuzzy import fuzz
import json

# Constants
HEADERS = {"Accept": "application/json"}
API_URL = "http://api.themoviedb.org"
API_SEARCH = "/3/search/movie"
API_MOVIE = "/3/movie/"
API_CONFIG = "/3/configuration"
FAILED_SELECT = None
EMPTY = ""

class MovieSearch:
    
    # Constructor
    def __init__(self, api_key):
        self.api_key = api_key
        self.poster_size = {'s':'w92','m':'w185','l':'w500','o':'original'}

        apiArgs = {'api_key' : self.api_key}
        query = API_URL + API_CONFIG + "?" + urlencode(apiArgs)
        apiRequest = Request(query, headers=HEADERS)
        result = urlopen(apiRequest).read()
        data = json.loads(result)
        
        self.base_url = data['images']['base_url']

    # User selection of movie
    def movieSelect(self, options):
        print "ID       TITLE                                                       RELEASE"
        print "-------- ----------------------------------------------------------- ----------"
        for movieId in options:
            movie = options[movieId]
            print "%s %s %s" % (movieId.rjust(8), (movie['title'][0:59].encode('ascii', 'replace')).ljust(59), movie['date'])

        inputId = FAILED_SELECT        
        while inputId not in options:
            inputId = raw_input("ENTER ID: ")
            
            if inputId == "-1":
                return FAILED_SELECT
        
        return inputId

    # Get id for movie title        
    def getId(self, title):
        apiArgs = {'api_key' : self.api_key, 'query' : title}
        query = API_URL + API_SEARCH + "?" + urlencode(apiArgs)
        apiRequest = Request(query, headers=HEADERS)
        result = urlopen(apiRequest).read()
        data = json.loads(result)
                
        movieId = None
        found = {}
        alt = {}
        
        for i in data['results']:
            if i is None:
                continue
            
            if fuzz.token_sort_ratio(title, i['title']) == 100:
                movieId = str(i['id'])
                found[movieId] = {'title' : i['title'], 'date' : i['release_date']}
            elif fuzz.token_sort_ratio(title, i['title']) > 85 and fuzz.partial_ratio(title, i['title']) > 90:
                altId = str(i['id'])
                alt[altId] = {'title' : i['title'], 'date' : i['release_date']}
        
        if len(found) == 1:
            return movieId
        elif len(found) > 1:
            print "DUPLICATES FOUND, ENTER THE ID OR -1 TO SKIP"
            movieId = self.movieSelect(found)
        elif len(alt) > 0:
            print "ALTERNATES FOUND, ENTER THE ID OR -1 TO SKIP"
            movieId = self.movieSelect(alt)
        
        return movieId

    # Get movie details
    def getDetails(self, movieId, append = None):
        apiArgs = {'api_key' : self.api_key, 'append_to_response' : append}
        query = API_URL + API_MOVIE + movieId + "?" + urlencode(apiArgs)
        apiRequest = Request(query, headers=HEADERS)
        result = urlopen(apiRequest).read()
        data = json.loads(result)
        
        genres = self.getGenres(data)
        cast = self.getCast(data)
        
        tempMovie = Movie()
        tempMovie.setId(movieId)
        tempMovie.setTitle(data['title'])
        tempMovie.setReleaseDate(data['release_date'])
        tempMovie.setGenre(genres)
        tempMovie.setCast(cast)
        tempMovie.setPosterPath(data['poster_path'])
        
        return tempMovie

    # Get genres as a list
    def getGenres(self, data):
        if 'genres' not in data:
            return EMPTY
        
        tempGenres = []
        movieGenres = data['genres']
        for genre in movieGenres:
            tempGenres.append(genre['name'])
        
        return tempGenres
    
    # Get cast as a list
    def getCast(self, data):
        if 'credits' not in data:
            return EMPTY
        
        tempCast = []
        movieCast = data['credits']['cast']
        for person in movieCast:
            tempCast.append(person['name'])
        
        return tempCast

    # Get poster image from url    
    def getPoster(self, file_path, size = "s"):
        file_path = str(file_path)
        
        url = self.base_url + self.poster_size[size] + file_path
        result = urlopen(url).read()
        
        return result
            
if __name__=='__main__':
    API_KEY = "447ecf40bf72a3fa6218f3024465a567"
    tempSearch = MovieSearch(API_KEY)
    tempMovieId = tempSearch.getId("Fight Club")
    
    if tempMovieId is not None:
        print tempMovieId
    
    tempMovie = tempSearch.getDetails(tempMovieId)
    print tempMovie.getString(';')
    
    tempMovie = tempSearch.getDetails(tempMovieId, "credits")
    print tempMovie.getString(';')   
    
    tempPath = tempMovie.getPosterPath()
    tempSearch.getPoster(tempPath)
    tempSearch.getPoster(tempPath, "s")
    tempSearch.getPoster(tempPath, "m")
    tempSearch.getPoster(tempPath, "l")
    tempSearch.getPoster(tempPath, "o")     