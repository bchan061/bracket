def getFilms():
    films = {}
    with open('top64.txt', encoding="utf-8") as filmsFile:
        for line in filmsFile:
            title = line.strip()
            films[title] = Film(title)
    return films
            
class Film():
    def __init__(self, name):
        self.name = name
        self.against = {}
        self.record = {}
        self.reset()

    def reset(self):
        self.wins = 0
        self.draws = 0
        self.loses = 0

    def addAgainst(self, other, forFilm, againstFilm):
        # Get the pair and make sure the first choice corresponds to this film
        self.against[other] = (forFilm, againstFilm)

    def calculateAbsoluteStats(self):
        for otherFilm in self.against:
            results = self.against[otherFilm]
            thisScore = results[0]
            otherScore = results[1]
            if thisScore > otherScore:
                self.wins += 1
                self.record[otherFilm] = 'Won'
            elif thisScore == otherScore:
                self.draws += 1
                self.record[otherFilm] = 'Draw'
            else:
                self.loses += 1
                self.record[otherFilm] = 'Lost'

    def calculateStats(self):
        for otherFilm in self.against:
            results = self.against[otherFilm]
            thisScore = results[0]
            otherScore = results[1]
            denom = thisScore + otherScore
            if denom == 0:
                denom = 1
            if thisScore > otherScore:
                self.wins += thisScore / denom
                self.record[otherFilm] = 'Won'
            elif thisScore == otherScore:
                self.draws += 1
                self.record[otherFilm] = 'Draw'
            else:
                self.loses += otherScore / denom
                self.record[otherFilm] = 'Lost'

    def getScore(self):
        return self.wins - self.loses

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
