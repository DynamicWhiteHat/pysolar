import matplotlib.pyplot as plt
import numpy as np
from skyfield.api import load

#Set up skyfield
ts = load.timescale()
t = ts.now()
planets = load('de440s.bsp')

#Load planets (barycenter is center taking into account moons and other orbital objects)
sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune = planets['sun'], planets['mercury barycenter'], planets['venus barycenter'], planets['earth'], planets['mars barycenter'], planets['jupiter barycenter'], planets['saturn barycenter'], planets['uranus barycenter'], planets['neptune barycenter']
planet = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

#Sizes and colors of planets
colors = ['yellow', 'dimgray', 'orangered', 'blue', 'firebrick', 'brown', 'darkkhaki', 'lightsteelblue', 'darkturquoise']
sizes = [9, 1, 3, 4, 2, 8, 7, 6, 5]
names = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
#Get 2D position using 3D z-axis
def get_position(planet):
    astrometric = planet.at(t)
    x, y, z = astrometric.position.au
    #Use distance formula to factor in z to 2D location
    r = np.sqrt(x**2+y**2+z**2)
    #Place (x,y) on unit circle and scale by r
    projected_x = x/np.sqrt(x**2+y**2)*r
    projected_y = y/np.sqrt(x**2+y**2)*r
    return projected_x, projected_y

def get_orbit(planet):
    astrometric = planet.at(t)
    x, y, z = astrometric.position.au
    #Use distance formula to factor in z to 2D location
    r = np.sqrt(x**2+y**2+z**2)
    #Create evenly spaced points on polygon with 500 sides
    theta = np.linspace(0, 2**np.pi, 500)
    #Place (x,y) on the t points
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    return x,y


#Create plot
fig, ax = plt.subplots(facecolor="black")
plt.axis("equal")

#Plot planets
for index, i in enumerate(planet):
    x,y= get_position(i)
    ax.scatter(x,y, c=colors[index], s=sizes[index]*45, label = names[index])

#Plot orbits
for i in planet:
    x,y=get_orbit(i)
    ax.plot(x,y, ls = '--', lw=2.5, c='white')

#Set up scroll
def on_scroll(event):
    #Check for scroll
    if event.button == 'up':
        scale_factor = 0.9
    elif event.button == 'down':
        scale_factor = 1.1
    else:
        scale_factor = 1.0
    #Get current graph limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    #Scale graph
    x_center = (xlim[0] + xlim[1]) / 2
    y_center = (ylim[0] + ylim[1]) / 2
    ax.set_xlim([x_center + (x - x_center) * scale_factor for x in xlim])
    ax.set_ylim([y_center + (y - y_center) * scale_factor for y in ylim])
    #Redraw graph
    plt.draw()

#Graph settings
ax.set_facecolor('black') #Color
ax.axis('off') #Hide Axis
fig.tight_layout() #Fill window
manager = plt.get_current_fig_manager() #Maximize window
manager.full_screen_toggle()

#Scrollable
fig.canvas.mpl_connect('scroll_event', on_scroll)

#Show legend and graph
ax.legend(labelspacing=1.5, borderpad=1)
plt.show()