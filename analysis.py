# this program should do some analysis of some csv data files

# this file is written as a script. run it in ipython with 
# %run analysis.py

import csv
import os
import numpy
import pylab

data_folder = "data"

import joystick
from joystick import Dataset, Datafile

ds = Dataset('data')

pylab.figure(1)
for df in ds.filter(songno=105, condition='i'):
    print df
    t = df.data['t']
    DotX = df.data['DotX']
    DotY = df.data['DotY']    
    pylab.title('Y vs t')
    pylab.plot(t,DotY, label=df.metadata['subject'])
#pylab.legend()
pylab.show()

# do animated plot
pylab.figure(2)
pylab.clf()
lines=dict()
colours={'i': 'r', 'l': 'b'} # instrumental = red, lyrics = blue

for df in ds.filter(songno=105):
    t = df.data['t']
    DotX = df.data['DotX']
    DotY = df.data['DotY']    
    col = colours[df.metadata['condition']]
    pylab.title('X vs Y')
    lines[df.filename], = pylab.plot(DotX,DotY,col+'o-', label=df.metadata['subject'])
    #pylab.legend()
    pylab.show()

pylab.ion() # turn interactive mode on
for i in range(2,len(df.data['DotX'])):
    for df in ds.filter(songno=105):
        DotX = df.data['DotX'][0:i]
        DotY = df.data['DotY'][0:i]
        lines[df.filename].set_data(DotX, DotY)
    pylab.draw()

pylab.ioff() # turn interactive mode off
