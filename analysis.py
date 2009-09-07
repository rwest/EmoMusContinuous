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
songno = 105 # Alanis Morrisette 


colours={'i': 'b', 
		 'l': 'r'} # instrumental = blue, lyrics = red
print "Reminder: Lyrics = Red, Instrumental = Blue"

#do 4 in one animated plot

#for i in [100]:
pylab.figure(3)
pylab.clf()
pylab.subplot(221)
pylab.axis([-400,400,-400,400])



sample_file = ds.filter(songno=songno).next()

pylab.subplot(224)
pylab.axis([0, sample_file.get_last_time(),-400,400])

for i in range(0, sample_file.get_frame_count(), 1 ):

	pylab.subplot(222).clear()
	pylab.subplot(223).clear()
	
	y_arrays=dict() # new dictionary for this time step
		
	for condition in ['i','l']:
		col = colours[condition]
		y_list=list()
		x_list=list()
		for df in ds.filter(songno=songno,condition=condition):
			t = df.data['t'][i]
			DotY = df.data['DotY'][i]
			DotX = df.data['DotX'][i]
			t = df.data['t'][i]
			y_list.append(DotY)
			x_list.append(DotX)
		y_array = numpy.array(y_list,dtype=float)
		x_array = numpy.array(x_list,dtype=float)
		
		# top right: Y value histogram
		pylab.subplot(222)
		pylab.hist(y_array, range=[-400,400], color=col, 
					  alpha=0.5, orientation='horizontal')
		pylab.axis([0,48,-400,400])
		# bottom left: X value histogram
		pylab.subplot(223)
		pylab.hist(x_array, range=[-400,400], color=col, 
					  alpha=0.5, orientation='vertical')
		pylab.axis([-400,400,0,48])
		
		# top left: XY scatter plot
		pylab.subplot(221)
		pylab.plot(x_array, y_array, col+'.')
		pylab.axis([-400,400,-400,400])
		
		# bottom right: mean and interquartile range
		pylab.subplot(224)
		y_array.sort()
		lower_quart = y_array[12] # check that these are right, I may have got them wrong
		upper_quart = y_array[-12] # remember counting starts from 0
		pylab.plot([t,t], [lower_quart,upper_quart], col+'-', alpha=0.1)
		# notice the *mean* is not necessarily within the interquartile range
		# because the outliers may pull it around a lot 
		# (obviously the median would be between them)
		pylab.plot(t,y_array.mean(), col+'.')
		pylab.axis([0, df.get_last_time(),-400,400])
		
		y_arrays[condition] = y_array
		
## it's a lot faster if you don't draw them! (ie. just save the png files)
#	 pylab.draw()
#	 pylab.show()

	# save the figure as a png to make a move
	pylab.savefig('combined%04d.png'%i)
	
	# do some maths!
	
	instrumental = y_arrays['i']
	lyric = y_arrays['l']
	
	print "At time = %.1fs the lyric is %f more arousing than the instrumental"%(
		t, lyric.mean()-instrumental.mean() )


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
pylab.draw()
for i in range(2, df.get_frame_count() ):
	for df in ds.filter(songno=105):
		DotX = df.data['DotX'][i-1:i]
		DotY = df.data['DotY'][i-1:i]
		line = lines[df.filename]
		line.set_data(DotX, DotY)
		axes.draw_artist(line)
	axes.figure.canvas.blit(axes.bbox) # just redraw the axes rectangle
pylab.ioff() # turn interactive mode off


# try a histogram
pylab.figure(3)
pylab.clf()
#for i in range(2,len(df.data['DotX'])):
for i in range(0,df.get_frame_count() ):
	pylab.clf()
	for condition in ['i','l']:
		y_list=list()
		for df in ds.filter(songno=105,condition=condition):
			t = df.data['t'][i]
			DotY = df.data['DotY'][i]
			y_list.append(DotY)
		y_array = numpy.array(y_list,dtype=float)
		pylab.hist(y_array, range=[-400,400], color=colours[condition], alpha=0.5)
	pylab.draw()
	pylab.show()
	# save the figure as a png to make a movie
	pylab.savefig('histogram%04d.png'%i)
		
		