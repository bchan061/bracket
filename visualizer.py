import pyglet
import question_reader
from pyglet.window import mouse
from visualizer_structures import Rectangle, Row, Camera

window = pyglet.window.Window(1280, 720)
components = []
rows = []
camera = Camera()

screen = ''

@window.event
def on_draw():
    global screen
    window.clear()
    if screen == 'rows' and rows is not None:
        for row in rows:
            row.draw(camera)
    for component in components:
        component.draw(camera)

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    camera.x += scroll_x * 25
    camera.y += scroll_y * 25
    
def changeScreen(newScreen):
    global screen
    screen = newScreen

def createRows():
    rows = []
    rowPadding = (5, 2)
    rowHeight = 33
    y = window.height - rowHeight
    for film in films:
        newRow = Row(films[film], Rectangle(rowPadding[0], y + rowPadding[1] / 2, window.width - rowPadding[0] * 2, rowHeight - rowPadding[1] / 2))
        rows.append(newRow)
        y -= rowHeight
    return rows

def init():
    global films
    global rows
    films = question_reader.createResponses()
    rows = createRows()

if __name__ == '__main__':
    init()
    changeScreen('rows')
    pyglet.app.run()
