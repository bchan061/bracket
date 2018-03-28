import pyglet

window = pyglet.window.Window()
components = []

@window.event
def on_draw():
    window.clear()
    for component in components:
        component.draw()
    

if __name__ == '__main__':
    
    components.append(label)
    pyglet.app.run()
