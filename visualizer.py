import pyglet

window = pyglet.window.Window()
components = []

@window.event
def on_draw():
    window.clear()
    for component in components:
        component.draw()
    

if __name__ == '__main__':
    label = pyglet.text.Label('Test',
                              font_name='Calibri',
                              font_size=16,
                              x=window.width // 2,
                              y=window.height // 2,
                              anchor_x='center',
                              anchor_y='center')
    components.append(label)
    pyglet.app.run()
