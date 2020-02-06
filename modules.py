import requests
import json
import textwrap

class myMenu:
    def __init__(self):
        self.userChoice = None
    
    def showMainMenu(self):
        print("""
Välj ett alternativ
1. Sök efter film
2. Visa senaste sökningar""")
    
    def userChoose(self):
        while True:
            self.showMainMenu()
            userChoice = UserInputInt()
            if userChoice == 0:
                exit()
            if userChoice == 1:
                ShowMovies()
            elif userChoice == 2:
                ShowMoviesHistory()


class Movies:
    def __init__(self, title, year, ratings, imdbID):
        self.title = title
        self.year = year
        self.ratings = ratings
        self.imdbID = imdbID
        self.movieDict = {"Title": self.title, "Year": self.year, "Ratings": self.ratings, "imdbID": self.imdbID}
        
        DisplayMovie(self.title, self.year, self.ratings)
        self.SaveMoviesHistory()
    
    def SaveMoviesHistory(self):
        with open("Movie_Searches.json", "r", encoding="utf-8") as fr:
            try:
                allLines = json.load(fr)
            except:
                print("FAILURE")
                allLines = []
            if len(allLines) > 9:
                del allLines[9]
            allLines.insert(0, self.movieDict)
        with open("Movie_Searches.json", "w", encoding="utf-8") as f:
            json.dump(allLines, f, indent=4, ensure_ascii=False)


def DisplayMovie(title, year, ratings):
    year = 'År: ' + year
    if len(title) > 24:
        lines = textwrap.wrap(title, 25)
        print(f'\n{lines[0]}\n{lines[1]:25} {year:>5}')
    else:
        print(f'\n{title:25} {year:>5}')
    print('-'*50)
    for x in ratings:
        x["Value"] = 'Betyg: ' + x["Value"]
        print(f'{x["Source"]:25} {x["Value"]:>5}')

def ShowMoviesHistory():
    with open("Movie_Searches.json", "r", encoding="utf-8") as f:
        indexedList = ParseMovies(json.load(f))
        userChoice = UserInputInt()
        if userChoice in indexedList:
            DisplayMovie(indexedList[userChoice]["Title"], indexedList[userChoice]["Year"], indexedList[userChoice]["Ratings"])

def GetMovieData(imdbID = None):
    if imdbID == None: # if request by title
        while True:
            movieTitle = input("Film: ")
            if movieTitle == "0":
                exit()
            response = requests.get(f'http://www.omdbapi.com/?apikey=3027195b&s={movieTitle}')
            data = response.json()
            if data['Response'] == 'True':
                break
            else:
                print("Filmen hittades inte")
    else: # if request by imdbID
        response = requests.get(f'http://www.omdbapi.com/?apikey=3027195b&i={imdbID}')
        data = response.json()
    return data

def ShowMovies(result = None):
    result = ParseMovies(result)
    if len(result) > 1:
        userChoice = UserInputInt()
        if userChoice in result:
            movieData = GetMovieData(result[userChoice]["imdbID"])
            Movies(movieData["Title"], movieData["Year"], movieData["Ratings"], movieData["imdbID"])
    
def ParseMovies(data = None):
    if data == None:
        data = GetMovieData()
        data = {i : movie for i, movie in enumerate(data['Search'], start=1)}
    else:
        data = {i : movie for i, movie in enumerate(data, start=1)}
    for i in data:
        print(f'{i:2}: {data[i]["Title"][:25]:25} {data[i]["Year"]}')
    return data

def UserInputInt():
    while True:
        try:
            print("\nAvsluta = 0")
            x = int(input("Ange en siffra: ")) 
            break
        except:
            print("Error, inte giltig siffra, försök igen")
    return x