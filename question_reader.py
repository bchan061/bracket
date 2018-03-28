import csv
import os
import pairer

films = []
responses = []
pairs = []

def hasStupidQuestion(part):
    return (part - 1) % 3 == 0

def getPart(filename):
    # Funny hack
    # Ending extension is '.csv' (4 characters)
    return int(filename[-6:-4].strip())

def addToResponses(answers):
    for i in range(len(answers)):
        answer = answers[i]
        equivalentPair = pairs[i]
        if answer == equivalentPair[1]:
            responses[i][0] += 1
        else:
            responses[i][1] += 1

if __name__ == '__main__':
    # Testing
    allQuestionFiles = os.listdir('Questions')
    pairs = pairer.getPairs()

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
                    answers = row[1:end]
                    addToResponses(answers)
                    
                count += 1
        print(responses[0:100])
        
