# this program should do some analysis of some csv data files

# this file is written as a script. 
# Suggested use: load ipython with ipython -pylab
# then run this with 
# %run analysis.py
# all the data will then be in memory for you to play with

import csv
import os

import pylab
import numpy

data_folder = "data"

import joystick
from joystick import Dataset, Datafile


ds = Dataset('data')

colours={'i': 'r', 'l': 'b'} # instrumental = red, lyrics = blue

# do a Y verses time plot
pylab.figure(1)
for df in ds.filter(songno=105):
    t = df.data['t']
    DotX = df.data['DotX']
    DotY = df.data['DotY']    
    col = colours[df.metadata['condition']]
    pylab.title('Y vs t')
    pylab.plot(t,DotY, col+'-', label=df.metadata['subject'])
#pylab.legend()
pylab.show()



# do an animated plot
# as described at http://www.scipy.org/Cookbook/Matplotlib/Animations
pylab.figure(2)
pylab.clf()
axes=pylab.subplot(111)
pylab.ion()
lines=dict()
for df in ds.filter(songno=105):
    t = df.data['t']
    DotX = df.data['DotX'][0:1]
    DotY = df.data['DotY'][0:1]  
    col = colours[df.metadata['condition']]
    pylab.title('X vs Y')
    lines[df.filename], = pylab.plot(DotX,DotY,col+'.-', label=df.metadata['subject'], animated=True)
    #pylab.legend()
axes.axis([-400,400,-400,400])
pylab.show()
pylab.ion() # turn interactive mode on
for i in range(2,len(df.data['DotX'])):
    for df in ds.filter(songno=105):
        DotX = df.data['DotX'][i-1:i]
        DotY = df.data['DotY'][i-1:i]
        line = lines[df.filename]
        line.set_data(DotX, DotY)
        axes.draw_artist(line)
    axes.figure.canvas.blit(axes.bbox) # just redraw the axes rectangle
pylab.ioff() # turn interactive mode off


# try a histogram
# I can't get histograms to work with my version of matplotlib
# so no idea if this code works:
pylab.figure(3)
#for i in range(2,len(df.data['DotX'])):
for i in [200]:
    y_list=list()
    for df in ds.filter(songno=105,condition='l'):
        t = df.data['t'][i]
        DotY = df.data['DotY'][i]
        y_list.append(DotY)
    y_array = numpy.array(y_list,dtype=float)
    pylab.hist(y_array)
    
        