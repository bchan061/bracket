import pyglet
import question_reader
import pyglet_utils
import pyglet.gl as pgl
from pyglet.window import mouse
from pyglet.text import Label
from visualizer_structures import Rectangle, ResultRow, RecordRow, Camera

films = {}
window = pyglet.window.Window(1280, 720, resizable=True)
movieLabel = Label('test',
                   font_name='Calibri',
                   font_size=36,
                   color=(255, 255, 255, 255),
                   x=window.width/2, y=window.height - 50,
                   anchor_x='center', anchor_y='center')
piMovieLabel = Label('test',
                     font_name='Calibri',
                     font_size=24,
                     color=(0, 0, 255, 255),
                     x=window.width/2, y=100,
                     anchor_x='center', anchor_y='center')
piMovieAgainstLabel = Label('test',
                            font_name='Calibri',
                            font_size=24,
                            color=(255, 0, 0, 255),
                            x=window.width/2, y=50,
                            anchor_x='center', anchor_y='center')
piMovie = None
piMovieAgainst = ''
recordRows = []
resultRows = []
camera = Camera()

screen = ''

@window.event
def on_resize(width, height):
    global recordRows
    global resultRows
    movieLabel.x = window.width / 2
    movieLabel.y = window.height - 50
    piMovieLabel.x = window.width / 2
    piMovieAgainstLabel.x = window.width / 2
    recordRows = []
    resultRows = []
    recordRows = createRecordRows()
    if screen != 'rows':
        resultRows = createResultRows(piMovie)

@window.event
def on_draw():
    global screen
    global recordRows
    global resultRows
    window.clear()
    
    if screen == 'rows':
        for row in recordRows:
            row.draw(camera)
    if screen == 'record':
        if resultRows is not None:
            for row in resultRows:
                row.draw(camera)
        movieLabel.x = window.width/2 - camera.x
        movieLabel.y = window.height - 50 - camera.y
        movieLabel.draw()
    if screen == 'pi':
        denom = sum(piMovie.against[piMovieAgainst])
        if denom == 0:
            denom = 1
        forDegrees = piMovie.against[piMovieAgainst][0] * 360 / denom
        
        pgl.glBegin(pgl.GL_TRIANGLE_FAN)
        pgl.glColor3f(0, 0, 1)
        forArc = pyglet_utils.arc(window.width / 2, window.height / 2, 100, 0, forDegrees)
        for vertex in forArc:
            pgl.glVertex2f(*vertex)
        pgl.glEnd()

        pgl.glBegin(pgl.GL_TRIANGLE_FAN)
        pgl.glColor3f(1, 0, 0)
        againstArc = pyglet_utils.arc(window.width / 2, window.height / 2, 100, forDegrees, 360)
        for vertex in againstArc:
            pgl.glVertex2f(*vertex)
        pgl.glEnd()
            
        movieLabel.x = window.width/2
        movieLabel.y = window.height - 50
        movieLabel.draw()
        piMovieLabel.draw()
        piMovieAgainstLabel.draw()
        

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    camera.x += scroll_x * 25
    camera.y += scroll_y * 25

@window.event
def on_mouse_release(x, y, button, modifiers):
    global recordRows
    global resultRows
    relativeX = x + camera.x
    relativeY = y + camera.y

    if button & mouse.LEFT:
        if screen == 'rows':
            for recordRow in recordRows:
                rect = recordRow.rectangle
                if rect.pointInRectangle((relativeX, relativeY)):
                    changeScreen('record')

                    movieLabel.text = recordRow.film.name
                    resultRows = []
                    resultRows = createResultRows(recordRow.film)
        elif screen == 'record':
            for resultRow in resultRows:
                rect = resultRow.rectangle
                if rect.pointInRectangle((relativeX, relativeY)):
                    changeScreen('pi')

                    global piMovie
                    global piMovieAgainst
                    global piMovieLabel
                    global piMovieAgainstLabel
                    piMovie = resultRow.film
                    piMovieAgainst = resultRow.otherFilmName
                    
                    denom = sum(piMovie.against[piMovieAgainst])
                    if denom == 0:
                        denom = 1
                    forPercent = piMovie.against[piMovieAgainst][0] / denom
                    
                    piMovieLabel.text = "{} ({} votes) [{:.2f}%]".format(
                        resultRow.film.name,
                        resultRow.film.against[resultRow.otherFilmName][0],
                        forPercent * 100
                        )
                    piMovieAgainstLabel.text = "{} ({} votes) [{:.2f}%]".format(
                        resultRow.otherFilmName,
                        resultRow.film.against[resultRow.otherFilmName][1],
                        (1 - forPercent) * 100
                        )
    elif button & mouse.RIGHT:
        if screen == 'record':
            changeScreen('rows')
        elif screen == 'pi':
            changeScreen('record')
        

def changeScreen(newScreen):
    global screen
    global camera
    screen = newScreen
    camera.x = 0
    camera.y = 0

def createRecordRows():
    rows = []
    rowPadding = (5, 2)
    rowHeight = 33
    y = window.height - rowHeight
    # Sort by score
    filmList = list(films.values())
    filmList.sort(key=(lambda x: x.getScore()), reverse = True)
    for i in range(len(filmList)):
        film = filmList[i]
        newRow = RecordRow(film, Rectangle(rowPadding[0], y + rowPadding[1] / 2, window.width - rowPadding[0] * 2, rowHeight - rowPadding[1] / 2))
        newRow.label.text = "{}. {}".format(i+1, newRow.label.text)
        rows.append(newRow)
        y -= rowHeight
    return rows

def createResultRows(film):
    rows = []
    rowPadding = (5, 2)
    rowHeight = 33
    y = window.height - 100 - rowHeight
    # Sort by score
    againstList = list(film.against.keys())
    againstList.sort(key=lambda x: films[x].getScore(), reverse=True)
    for i in range(len(againstList)):
        other = againstList[i]
        newRow = ResultRow(film, other, Rectangle(rowPadding[0], y + rowPadding[1] / 2, window.width - rowPadding[0] * 2, rowHeight - rowPadding[1] / 2))
        rows.append(newRow)
        y -= rowHeight
    return rows

def init():
    global films
    global recordRows
    films = question_reader.createResponses()
    recordRows = createRecordRows()

if __name__ == '__main__':
    init()
    changeScreen('rows')
    pyglet.app.run()
