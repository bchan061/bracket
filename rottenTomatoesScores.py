import csv

def getPairsOfScores():
    filmScores = {}
    with open('rottentomatoes.csv', encoding="utf-8") as rtScoresFile:
        rtScoresCsv = csv.reader(rtScoresFile, delimiter=',')
        count = 0
        for row in rtScoresCsv:
            # Disregard the topics.
            if count > 0:
                filmName = row[0].strip()
                filmScore = int(row[1].strip())
                filmScores[filmName] = filmScore
            count += 1
    return filmScores

if __name__ == '__main__':
    # Testing
    filmScores = getPairsOfScores()
    print(filmScores['Toy Story 3'])
    
