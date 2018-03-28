import pyglet
from pyglet.text import Label

class DrawableComponent():
    def draw(self, camera):
        pass

class Camera():
    def __init__(self):
        self.x = 0
        self.y = 0

class Rectangle(DrawableComponent):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @staticmethod
    def startDrawing():
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)

    @staticmethod
    def endDrawing():
        pyglet.gl.glEnd()

    def draw(self, camera):
        pyglet.gl.glVertex2f(self.x - camera.x, self.y + self.height - camera.y)
        pyglet.gl.glVertex2f(self.x + self.width - camera.x, self.y + self.height - camera.y)
        pyglet.gl.glVertex2f(self.x + self.width - camera.x, self.y - camera.y)
        pyglet.gl.glVertex2f(self.x - camera.x, self.y - camera.y)

    def __str__(self):
        return "({}, {}, {}, {})".format(self.x, self.y, self.width, self.height)

class Row(DrawableComponent):
    def __init__(self, film, rectangle):
        self.film = film
        self.rectangle = rectangle
        self.label = Label(self.film.name,
                           font_name='Calibri',
                           font_size=18,
                           color=(0, 0, 0, 255),
                           x=self.rectangle.x, y=(self.rectangle.y + self.rectangle.height / 2),
                           anchor_x='left', anchor_y='center')
        self.record = Label(self.film.name,
                            font_name='Calibri',
                            font_size=18,
                            color=(0, 0, 0, 255),
                            x=self.rectangle.x + self.rectangle.width, y=(self.rectangle.y + self.rectangle.height / 2),
                            anchor_x='right', anchor_y='center')

    def draw(self, camera):
        self.label.x = self.rectangle.x - camera.x
        self.label.y = (self.rectangle.y + self.rectangle.height / 2) - camera.y
        self.record.x = self.rectangle.x + self.rectangle.width - camera.x
        self.record.y = (self.rectangle.y + self.rectangle.height / 2) - camera.y
        self.record.text = "{:.2f} - {:.2f} - {:.2f}".format(self.film.wins, self.film.draws, self.film.loses)
        
        Rectangle.startDrawing()
        pyglet.gl.glColor3f(245 / 255, 245 / 255, 220 / 255)
        self.rectangle.draw(camera)
        Rectangle.endDrawing()
        self.label.draw()
        self.record.draw()
