import matplotlib.pyplot as plt
import numpy as np
from skyfield.api import load
import streamlit as st
import mpld3
import streamlit.components.v1 as components
from datetime import datetime
import time

# Set up skyfield
ts = load.timescale()
t = ts.now()
planets = load('de440s.bsp')

# Load planets (barycenter is center taking into account moons and other orbital objects)
sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune = planets['sun'], planets['mercury barycenter'], planets['venus barycenter'], planets['earth'], planets['mars barycenter'], planets['jupiter barycenter'], planets['saturn barycenter'], planets['uranus barycenter'], planets['neptune barycenter']
planet = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

# Sizes and colors of planets
colors = ['yellow', 'dimgray', 'orangered', 'blue', 'firebrick', 'brown', 'darkkhaki', 'lightsteelblue', 'darkturquoise']
sizes = [9, 1, 3, 4, 2, 8, 7, 6, 5]
names = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

# Get 2D position using 3D z-axis
def get_position(planet):
    astrometric = planet.at(t)
    x, y, z = astrometric.position.au
    # Use distance formula to factor in z to 2D location
    r = np.sqrt(x**2 + y**2 + z**2)
    # Place (x, y) on unit circle and scale by r
    projected_x = x / np.sqrt(x**2 + y**2) * r
    projected_y = y / np.sqrt(x**2 + y**2) * r
    return projected_x, projected_y

def get_orbit(planet):
    astrometric = planet.at(t)
    x, y, z = astrometric.position.au
    # Use distance formula to factor in z to 2D location
    r = np.sqrt(x**2 + y**2 + z**2)
    # Create evenly spaced points on polygon with 500 sides
    theta = np.linspace(0, 2 * np.pi, 500)
    # Place (x, y) on the t points
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


# Create plot
fig, ax = plt.subplots(figsize=(13,8), facecolor="black")  # Adjusted figsize
plt.axis("equal")

# Plot planets
for index, i in enumerate(planet):
    x, y = get_position(i)
    ax.scatter(x, y, c=colors[index], s=sizes[index] * 15, label=names[index])

# Plot orbits
for i in planet:
    x, y = get_orbit(i)
    ax.plot(x, y, ls='--', lw=2.5, c='white')

# Set up scroll
def on_scroll(event):
    # Check for scroll
    if event.button == 'up':
        scale_factor = 0.9
    elif event.button == 'down':
        scale_factor = 1.1
    else:
        scale_factor = 1.0
    # Get current graph limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    # Scale graph
    x_center = (xlim[0] + xlim[1]) / 2
    y_center = (ylim[0] + ylim[1]) / 2
    ax.set_xlim([x_center + (x - x_center) * scale_factor for x in xlim])
    ax.set_ylim([y_center + (y - y_center) * scale_factor for y in ylim])
    # Redraw graph
    plt.draw()

# Graph settings
ax.set_facecolor('black')  # Color
ax.axis('off')  # Hide Axis
fig.tight_layout()  # Fill window
manager = plt.get_current_fig_manager()  # Maximize window
manager.full_screen_toggle()

# Hide axis numbers
ax.set_xticks([])  
ax.set_yticks([])

# Scrollable
fig.canvas.mpl_connect('scroll_event', on_scroll)

# Show legend and graph
ax.legend(labelspacing=1.5, borderpad=1)

# Show on Streamlit
st.set_page_config(
   page_title="PySolar - A Real-Time Interactive Solar System",
   page_icon="🛰️",
   layout="wide",
   initial_sidebar_state="expanded",
)
with st.container():
    st.markdown("<h1 style='text-align: center;'>PySolar - A Real-Time Interactive Solar System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Use the tools at the bottom left of the graph to zoom in and out</p>", unsafe_allow_html=True)
    time_placeholder = st.empty()



# Show graph
html = mpld3.fig_to_html(fig)
components.html(html, height=900, width=1300)  # Adjusted height for better view

while True:
    current_time = datetime.now()
    time_placeholder.markdown(f"<p style='text-align: center; background-color: #f8f9fb; border-radius: 5em; color: #09ab3b;'>{current_time}</p>", unsafe_allow_html=True)
    time.sleep(1) 
