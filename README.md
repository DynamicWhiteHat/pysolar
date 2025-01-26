## Update: Now hosted online using Streamlit. Visit: https://pysolar.streamlit.app/

# pysolar
 - A simple real-time solar system viewer written 100% in Python
 - Uses the Skyfield library to pull data from JPL's Development Ephemeris series de440s.bsp file, which includes data from 1849 to 2150
 - Displays the system in a scrollable matplotlib window

# Usage
- Locally:
  - Download the packages from requirements.txt
  - Open the main.py file in any IDE of your choice with python 1.12 or lower, **Skyfield does not support Python 1.13 as of December 2024,** and add the following line at the end:
  - <pre>plt.show()</pre>
  - Run the program to download the required files
  - Once the de400s.bsp file is downloaded, a matplotlib window will open
  - Use your mouse to scroll in and out to see the planets

# Understanding the math
Skyfield returns the astronomical positions of the planets as 3D space, (x,y,z), points. The get_position function turns this 3D point into a 2D point by calculating the radius by using the distance formula:

$$\sqrt{\left(x_{2}-x_{1}\right)^{2}+\left(y_{2}-y_{1}\right)^{2}+\left(z_{2}-z_{1}\right)^{2}}$$

and using this radius to scale points x and y on a unit circle with radius of 1. These points can now be placed on a 2D graph and accurately represent the distance between the Sun and the planet.
