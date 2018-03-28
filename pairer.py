import itertools
films = []

def getPairs():
    films = []
    with open('top64.txt', encoding='utf-8') as top64File:
        for line in top64File:
            films.append(line)

    pairs = itertools.combinations(films, r=2)

    returnedPairs = []
    count = 1
    for pair in pairs:
        topic = "Question {}".format(count)
        item1 = pair[0].strip()
        item2 = pair[1].strip()
        returnedPairs.append((topic, item1, item2))

        count += 1
    return returnedPairs

if __name__ == '__main__':
    print("Opening top films...", end='')
    with open('top64.txt', encoding='utf-8') as top64File:
        for line in top64File:
            films.append(line)
    print("Success")

    print("Creating unique pairs...", end='')
    pairs = itertools.combinations(films, r=2)
    print("Success")

    print("Writing all pairs...", end='')
    with open('pairs.csv', 'w', encoding='utf-8') as pairsFile:
        count = 1
        for pair in pairs:
            item1 = pair[0].strip()
            item2 = pair[1].strip()

            line = '"Question {}|{}|{}"\n'.format(count, item1, item2)
            pairsFile.write(line)

            count += 1
    print("Success")
