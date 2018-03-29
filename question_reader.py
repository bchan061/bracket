import csv
import os
import pairer
import film

films = {}
responses = []
pairs = []

def hasStupidQuestion(part):
    return (part - 1) % 3 == 0

def getPart(filename):
    # Funny hack
    # Ending extension is '.csv' (4 characters)
    return int(filename[-6:-4].strip())

def addToResponses(answers, part):
    offset = (part - 1) * 100
    for i in range(len(answers)):
        answer = answers[i]
        addToResponse(i + offset, answer)

def addToResponse(i, answer):
    equivalentPair = pairs[i]
    if answer == equivalentPair[1]:
        responses[i][0] += 1
    else:
        responses[i][1] += 1

def createResponses():
    global films
    global responses
    global pairs
    
    allQuestionFiles = os.listdir('Questions')
    allQuestionFiles.sort(key=lambda x: getPart(x))
    pairs = pairer.getPairs()
    films = film.getFilms()

    for pair in pairs:
        responses.append([0, 0])
    
    for questionFileName in allQuestionFiles:
        questionFileName = 'Questions/' + questionFileName
        partNumber = getPart(questionFileName)
        with open(questionFileName, encoding='utf-8') as questionFile:
            questionFileReader = csv.reader(questionFile, delimiter=',')
            count = 0
            for row in questionFileReader:
                # Disregard the topics.
                if count >= 1:
                    # Disregard the date and any stupid questions.
                    end = len(row)
                    if hasStupidQuestion(partNumber):
                        end -= 1
                    # I screwed up, left comments in part 20
                    if partNumber == 20:
                        end -= 1
                    # End has 2 comments
                    if partNumber == 21:
                        end -= 2
                    answers = row[1:end]
                    addToResponses(answers, partNumber)
                    
                count += 1

    compileResponsesIntoFilms()
    computeStats()
    return films

def compileResponsesIntoFilms():
    for i in range(len(responses)):
        response = responses[i]
        pair = pairs[i]
        firstFilm = pair[1]
        secondFilm = pair[2]
        films[firstFilm].addAgainst(secondFilm, response[0], response[1])
        films[secondFilm].addAgainst(firstFilm, response[1], response[0])

def computeStats():
    for film in films:
        films[film].calculateStats()
        
def computeAbsoluteStats():
    for film in films:
        films[film].calculateAbsoluteStats()

if __name__ == '__main__':
    # Testing
    createResponses()
    print(responses[2000])
