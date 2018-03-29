import matplotlib.pyplot as plt
import question_reader
import rottenTomatoesScores
from math import sqrt
from scipy.stats import linregress

fig = None
ax = None
scatter = None
annot = None
pos = (0, 0)
rtScores = []
films = []
scores = []

def update_annot(ind):
    global pos
    hoveredOver = list(ind['ind'])
    text = ''
    for film in hoveredOver:
        if text != '':
            text += ', '
        text += "{} [RT: {}, Our: {:.2f}]".format(films[film], rtScores[film], scores[film])
    annot.xy = pos
    annot.xytext = (pos[0], pos[1] - 5)
    annot.set_text(text)

# Stolen from https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib
def hover(event):
    global pos
    visible = annot.get_visible()
    if event.inaxes == ax:
        pos = [event.xdata, event.ydata]
        cont, ind = scatter.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if visible:
                annot.set_visible(False)
                fig.canvas.draw_idle()

if __name__ == '__main__':
    filmScores = rottenTomatoesScores.getPairsOfScores()
    ourFilmScores = question_reader.createResponses()
    xKeys = list(ourFilmScores.keys())
    xData = []
    yData = [film.getScore() for film in ourFilmScores.values()]
    for i in range(len(xKeys)):
        filmName = xKeys[i]
        films.append(filmName)
        scores.append(yData[i])
        rtScores.append(filmScores[filmName])
        xData.append(filmScores[filmName])

    slope, intercept, r_value, p_value, stderr = linregress(xData, yData)
    
    fig, ax = plt.subplots()
    
    scatter = ax.scatter(xData, yData, label='Data')
    annot = ax.annotate("",
                        xy = (0, 0),
                        xytext = (20, 20),
                        textcoords = 'offset points',
                        bbox = dict(boxstyle = 'round', fc = 'w'),
                        arrowprops = dict(arrowstyle = "->"))
    annot.set_visible(False)
    fig.canvas.mpl_connect('motion_notify_event', hover)
    plt.xlabel('Rotten Tomatoes score')
    plt.ylabel('Our score')
    plt.title('Our score in comparison with Rotten Tomatoes\'s score')
    start = (0, intercept)
    end = (100, slope * 100 + intercept)
    # pyplot suk
    lsrl = plt.plot(end, start, color='black', label='LSRL (r^2 = {:.3f})'.format(r_value * r_value))
    ax.legend()
    plt.show()
