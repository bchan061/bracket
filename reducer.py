import csv
films = []
strikedOffFilms = {}

if __name__ == '__main__':
    # CREATING LIST OF FILMS
    print("Creating list of films... ", end='')
    with open('films.txt', encoding="utf-8") as filmsFile:
        for line in filmsFile:
            films.append(line.strip())
    print("Success")

    # IMPORTING CSV...
    print("Curating responses...", end='')
    with open('reducing.csv', encoding="utf-8") as responsesFile:
        responsesReader = csv.reader(responsesFile, delimiter=';')
        responses = []
        count = 0
        for row in responsesReader:
            # Disregard the top response, listing out the order.
            if count > 0:
                # Disregard the name at the end
                responses.append(row[1:len(row) - 1])
            count += 1
        for response in responses:
            for item in response:
                if item not in strikedOffFilms:
                    strikedOffFilms[item] = 0
                strikedOffFilms[item] += 1

    print("Success")

    print("Producing final list... ", end='')
    # Sort the films by the amount of strike offs
    strikedOffFilmsList = sorted(strikedOffFilms, key=strikedOffFilms.get, reverse=True)

    print(strikedOffFilms.get('Snow White and the Seven Dwarves'))

    # Get the bottom 64.
    bottom64 = strikedOffFilmsList[0:64]

    # Remove the bottom 64 from the films list.
    for badFilm in bottom64:
        films.remove(badFilm)
    print("Success")

    # We're done!
    with open('top64.txt', 'w', encoding="utf-8") as finalFilms:
        for goodFilm in films:
            line = goodFilm + '\n'
            finalFilms.write(line)

    print("Printed to top64.txt")
