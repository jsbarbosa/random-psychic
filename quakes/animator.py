#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  animator.py
#  
#  Copyright 2016 Juan Barbosa <juan@Lenovo-U410>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import numpy as np
from textwrap import wrap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid.inset_locator import inset_axes

def dataloader(name = "signif.txt"):
    data = np.genfromtxt(name, delimiter="\t", usecols=[2, 9, 20, 21], skip_header=True)
    pos = np.where(data[:,1] == data[:,1])[0]
    years = data[pos,0]
    intensities = data[pos, 1]
    sizes = np.log(intensities)*5
    x = data[pos,3]
    y = data[pos,2]
    
    n = len(x)
    
    cite = "National Geophysical Data Center / World Data Service (NGDC/WDS): Significant Earthquake Database. National Geophysical Data Center, NOAA. doi:10.7289/V5TD9V7K"
    title = "\n".join(wrap(cite, 70))
    
    fig, ax = plt.subplots(figsize=(16,9))
    
    my_map = Basemap(projection='robin', lon_0=0, resolution='l', ax=ax)

    my_map.bluemarble()
    my_map.drawcountries()
    
    ax2 = inset_axes(ax, width="30%", height=3.0, loc=3)
    
    xs, ys = my_map(x, y)
    points = my_map.scatter(xs, ys, marker='o', c = intensities, cmap = 'OrRd', s = sizes*2, alpha = 0.5, lw = 0.1)
    text = ax.annotate('', xy=(0.45, 0.01), xycoords='axes fraction')
    points.set_offsets(np.zeros((1,2)))
    fps = 1/20
    duration = 30

    step = int(np.ceil(n*fps/duration))
    frames = int(np.ceil(n/step))
    
    fps = frames/duration
    
    data = np.hstack((xs[:,np.newaxis], ys[:, np.newaxis]))

    def update(i):
        ax2.cla()
        log = -3*i*360/frames + 720
        
        globe = Basemap(projection='ortho', lat_0=0, lon_0=log, resolution='c', ax=ax2)
        globe.bluemarble()
        globe.drawcountries()

        xs, ys = globe(x, y)
        globe.scatter(xs, ys, c = intensities, cmap='OrRd', s = sizes, alpha = 0.5, lw = 0.1)
        
        p = i*step
        points.set_offsets(data[:p])
        if years[p] == years[p]:
            text.set_text("Year: %d"%(years[p]))
        
        return points, text, globe
    
    cbaxes = fig.add_axes([0.9, 0.1, 0.03, 0.8]) 
    cbar = plt.colorbar(points, cax = cbaxes)
     
    cbar.ax.set_xlabel('Intensity')
    cbar.set_alpha(1)
    cbar.draw_all()
    
    ax.set_title(title, fontsize=10)
 
    ani = animation.FuncAnimation(fig, update, frames = frames)
    
    return ani, fps

if __name__ == "__main__":
    ani, fps = dataloader()
    ani.save('Quakes.mp4', dpi=120, codec='h264', fps = fps)
#    plt.show()
