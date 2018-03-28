from math import cos, sin, radians
import pyglet
import pyglet.gl as pgl

# Borrowed from libgdx
def definedArc(x, y, radius, angleStart, angleEnd, numPoints):
    vertices = []
    angleRange = angleEnd - angleStart
    angleStart = radians(angleStart)
    angleRange = radians(angleRange)
    
    cosAngle = cos(angleRange / numPoints)
    sinAngle = sin(angleRange / numPoints)

    cx = radius * cos(angleStart)
    cy = radius * sin(angleStart)
    vertices.append((x, y))
    for i in range(numPoints):
        vertices.append((x + cx, y + cy))

        temp = cx
        cx = cosAngle * cx - sinAngle * cy
        cy = sinAngle * temp + cosAngle * cy
    vertices.append((x + cx, y + cy))
        
    return vertices
def arc(centerX, centerY, radius, angleStart, angleEnd):
    numPoints = int(6 * (radius) ** (1/3) * (angleEnd - angleStart) / 360) + 1
    return definedArc(centerX, centerY, radius, angleStart, angleEnd, numPoints)
def drawArc(arc, color):
    pgl.glColor3f(color[0], color[1], color[2])
    pgl.glBegin(pgl.GL_TRIANGLE_FAN)
    for vertex in arc:
        pgl.glVertex2f(vertex[0], vertex[1])
    pgl.glEnd()

if __name__ == '__main__':
    # Testing arc
    window = pyglet.window.Window()
    testArc = arc(window.width // 2,
                  window.height // 2,
                  100,
                  0,
                  135)

    @window.event
    def on_draw():
        pgl.glClear(pgl.GL_COLOR_BUFFER_BIT)
        pgl.glColor3f(0, 1, 1)
        pgl.glBegin(pgl.GL_TRIANGLE_FAN)
        for vertex in testArc:
            pgl.glVertex2f(vertex[0], vertex[1])
        pgl.glEnd()

    pyglet.app.run()

